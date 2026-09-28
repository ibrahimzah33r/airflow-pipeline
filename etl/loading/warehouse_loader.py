import os
from typing import Any

import psycopg
from dotenv import load_dotenv


load_dotenv(".env")


def get_warehouse_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=os.environ["WAREHOUSE_HOST"],
        port=os.environ["WAREHOUSE_PORT"],
        dbname=os.environ["WAREHOUSE_POSTGRES_DB"],
        user=os.environ["WAREHOUSE_POSTGRES_USER"],
        password=os.environ["WAREHOUSE_POSTGRES_PASSWORD"],
    )


def load_market_records(
    records: list[dict[str, Any]],
) -> int:
    inserted_count = 0

    with get_warehouse_connection() as connection:
        with connection.cursor() as cursor:
            for record in records:
                cursor.execute(
                    """
                    INSERT INTO dim_asset (
                        external_id,
                        symbol,
                        name
                    )
                    VALUES (%s, %s, %s)
                    ON CONFLICT (external_id)
                    DO UPDATE SET
                        symbol = EXCLUDED.symbol,
                        name = EXCLUDED.name
                    RETURNING id
                    """,
                    (
                        record["external_id"],
                        record["symbol"],
                        record["name"],
                    ),
                )

                asset_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO fact_market_price (
                        asset_id,
                        observed_at,
                        price_usd,
                        volume_24h_usd
                    )
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (asset_id, observed_at)
                    DO NOTHING
                    """,
                    (
                        asset_id,
                        record["observed_at"],
                        record["price_usd"],
                        record["volume_24h_usd"],
                    ),
                )

                inserted_count += cursor.rowcount

    return inserted_count