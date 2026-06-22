import hashlib
import json
import platform
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


class ArtifactError(RuntimeError):
    """Raised when a required dashboard artifact is missing or invalid."""


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksum(artifact_path: Path, checksum_path: Path) -> str:
    checksum = sha256_file(artifact_path)
    checksum_path.write_text(f"{checksum}  {artifact_path.name}\n", encoding="ascii")
    return checksum


def verify_checksum(artifact_path: Path, checksum_path: Path) -> str:
    if not artifact_path.exists():
        raise ArtifactError(f"Required artifact is missing: {artifact_path}")
    if not checksum_path.exists():
        raise ArtifactError(
            f"Model checksum is missing: {checksum_path}. Rebuild artifacts before running the app."
        )

    checksum_parts = checksum_path.read_text(encoding="ascii").strip().split()
    if not checksum_parts or len(checksum_parts[0]) != 64:
        raise ArtifactError(f"Model checksum file is invalid: {checksum_path}")
    expected = checksum_parts[0].lower()
    actual = sha256_file(artifact_path)
    if expected != actual:
        raise ArtifactError(
            "The saved model failed its integrity check. Do not load it; restore or rebuild "
            f"{artifact_path.name}."
        )
    return actual


def package_versions(packages: list[str]) -> dict[str, str]:
    versions = {}
    for package in packages:
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "not-installed"
    return versions


def build_provenance(
    model_path: Path,
    data_path: Path,
    source_data: str,
    model_checksum: str,
) -> dict:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_data": source_data,
        "model_file": model_path.name,
        "model_sha256": model_checksum,
        "processed_data_file": data_path.name,
        "processed_data_sha256": sha256_file(data_path),
        "python_version": platform.python_version(),
        "packages": package_versions(
            ["catboost", "numpy", "pandas", "plotly", "scikit-learn", "shap", "streamlit"]
        ),
    }


def write_provenance(path: Path, provenance: dict) -> None:
    path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
