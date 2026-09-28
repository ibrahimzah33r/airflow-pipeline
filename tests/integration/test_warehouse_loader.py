from datetime import datetime, timezone
from uuid import uuid4

from etl.loading.warehouse_loader import (
    get_warehouse_connection,
    load_market_records,
)


def test_loading_same_record_twice_is_idempotent():
    unique_id = uuid4().hex[:8]

    external_id = f"test-asset-{unique_id}"
    observed_at = datetime(
        2026,
        1,
        1,
        12,
        0,
        0,
        tzinfo=timezone.utc,
    ).isoformat()

    records = [
        {
            "external_id": external_id,
            "symbol": "TEST",
            "name": "Test Asset",
            "observed_at": observed_at,
            "price_usd": 100.0,
            "volume_24h_usd": 1000.0,
        }
    ]

    try:
        first_count = load_market_records(records)
        second_count = load_market_records(records)

        assert first_count == 1
        assert second_count == 0

    finally:
        with get_warehouse_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM fact_market_price
                    WHERE asset_id = (
                        SELECT id
                        FROM dim_asset
                        WHERE external_id = %s
                    )
                    """,
                    (external_id,),
                )

                cursor.execute(
                    """
                    DELETE FROM dim_asset
                    WHERE external_id = %s
                    """,
                    (external_id,),
                )