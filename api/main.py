from typing import Annotated

import psycopg
from fastapi import Depends, FastAPI

from api.db import get_db


app = FastAPI(
    title="Market Pipeline API",
    version="1.0.0",
)


DatabaseConnection = Annotated[
    psycopg.Connection,
    Depends(get_db),
]


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }


@app.get("/market/latest")
def latest_market_data(
    connection: DatabaseConnection,
) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT ON (d.id)
                d.external_id,
                d.symbol,
                d.name,
                f.observed_at,
                f.price_usd,
                f.volume_24h_usd
            FROM fact_market_price f
            JOIN dim_asset d
                ON d.id = f.asset_id
            ORDER BY
                d.id,
                f.observed_at DESC
            """
        )

        rows = cursor.fetchall()

    return [
        {
            "external_id": row[0],
            "symbol": row[1],
            "name": row[2],
            "observed_at": row[3],
            "price_usd": row[4],
            "volume_24h_usd": row[5],
        }
        for row in rows
    ]