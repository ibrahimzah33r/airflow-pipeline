from datetime import datetime, timezone

from etl.ingestion.kraken_api import fetch_market_data
from etl.storage.minio_client import store_raw_json


def ingest_market_data() -> str:
    collected_at = datetime.now(timezone.utc)

    data = fetch_market_data()

    object_name = store_raw_json(
        data=data,
        source="kraken",
        collected_at=collected_at,
    )

    return object_name