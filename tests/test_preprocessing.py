import pandas as pd

from src.preprocessing.build_artifacts import create_target


def test_create_target_from_current_financial_service_usage() -> None:
    source = pd.DataFrame(
        {
            "bank_usage": ["Never had", "Currently have", None],
            "mobile_money_usage": ["Never had", "Never had", "Currently have"],
            "insurance_usage": ["Never had", "Never had", None],
        }
    )

    result = create_target(source)

    assert result["financially_included"].tolist() == [0, 1, 1]
