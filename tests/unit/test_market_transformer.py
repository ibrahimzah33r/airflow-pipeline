from datetime import datetime, timezone

from etl.transformation.market_transformer import (
    get_observed_at_from_object_name,
    transform_market_data,
)


def test_object_name_produces_stable_timestamp():
    object_name = "raw/kraken/2026/09/28/140146.json"

    result = get_observed_at_from_object_name(
        object_name
    )

    assert result == datetime(
        2026,
        9,
        28,
        14,
        1,
        46,
        tzinfo=timezone.utc,
    )


def test_transform_market_data():
    raw_data = {
        "result": {
            "XXBTZUSD": {
                "c": ["80000.00", "1"],
                "v": ["10", "20"],
            }
        }
    }

    observed_at = datetime(
        2026,
        9,
        28,
        14,
        1,
        46,
        tzinfo=timezone.utc,
    )

    records = transform_market_data(
        raw_data,
        observed_at,
    )

    assert len(records) == 1

    record = records[0]

    assert record["external_id"] == "bitcoin"
    assert record["symbol"] == "BTC"
    assert record["price_usd"] == 80000.0
    assert record["volume_24h_usd"] == 1600000.0