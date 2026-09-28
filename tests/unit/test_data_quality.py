import pytest

from etl.transformation.data_quality import (
    validate_market_records,
)


def valid_record() -> dict:
    return {
        "external_id": "bitcoin",
        "symbol": "BTC",
        "name": "Bitcoin",
        "observed_at": "2026-09-28T14:01:46+00:00",
        "price_usd": 80000.0,
        "volume_24h_usd": 1000000.0,
    }


def test_valid_market_record_passes():
    records = [valid_record()]

    result = validate_market_records(records)

    assert result == records


def test_negative_price_fails():
    record = valid_record()
    record["price_usd"] = -1

    with pytest.raises(
        ValueError,
        match="Invalid price",
    ):
        validate_market_records([record])


def test_duplicate_asset_fails():
    record = valid_record()

    with pytest.raises(
        ValueError,
        match="Duplicate asset",
    ):
        validate_market_records(
            [record, record.copy()]
        )


def test_missing_field_fails():
    record = valid_record()
    del record["symbol"]

    with pytest.raises(
        ValueError,
        match="Missing required fields",
    ):
        validate_market_records([record])