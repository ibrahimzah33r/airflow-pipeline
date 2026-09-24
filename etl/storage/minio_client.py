import json
import os
from datetime import datetime, timezone
from io import BytesIO
from typing import Any

from dotenv import load_dotenv
from minio import Minio


load_dotenv()


def get_minio_client() -> Minio:
    endpoint = os.environ["MINIO_ENDPOINT"]
    access_key = os.environ["MINIO_ROOT_USER"]
    secret_key = os.environ["MINIO_ROOT_PASSWORD"]
    secure = os.getenv("MINIO_SECURE", "false").lower() == "true"

    return Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure,
    )


def ensure_bucket_exists(client: Minio, bucket_name: str) -> None:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)


def store_raw_json(
    data: Any,
    source: str,
    collected_at: datetime | None = None,
) -> str:
    client = get_minio_client()

    bucket_name = os.getenv(
        "MINIO_RAW_BUCKET",
        "raw-market-data",
    )

    ensure_bucket_exists(client, bucket_name)

    timestamp = collected_at or datetime.now(timezone.utc)

    object_name = (
        f"raw/{source}/"
        f"{timestamp:%Y/%m/%d}/"
        f"{timestamp:%H%M%S}.json"
    )

    json_bytes = json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")

    json_stream = BytesIO(json_bytes)

    client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=json_stream,
        length=len(json_bytes),
        content_type="application/json",
    )

    return object_name