import pytest

import src.artifacts as artifacts
from src.artifacts import ArtifactError, verify_checksum
from src.config import MODEL_CHECKSUM_PATH, MODEL_PATH


def test_repository_model_checksum() -> None:
    expected = MODEL_CHECKSUM_PATH.read_text(encoding="ascii").split()[0]
    assert verify_checksum(MODEL_PATH, MODEL_CHECKSUM_PATH) == expected


def test_checksum_rejects_modified_artifact(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(artifacts, "sha256_file", lambda _: "0" * 64)

    with pytest.raises(ArtifactError, match="failed its integrity check"):
        verify_checksum(MODEL_PATH, MODEL_CHECKSUM_PATH)
