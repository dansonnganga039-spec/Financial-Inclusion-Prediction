from src.data import load_county_geojson, load_data, load_metrics, load_model


def test_repository_artifacts_load() -> None:
    assert not load_data().empty
    assert load_metrics()["features"]
    assert load_model().named_steps
    assert load_county_geojson()["features"]
