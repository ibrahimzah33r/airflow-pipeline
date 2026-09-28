import logging

import pendulum
from airflow.sdk import dag, task

from etl.ingestion.market_ingestion import ingest_market_data
from etl.loading.warehouse_loader import load_market_records
from etl.storage.minio_client import read_json_object
from etl.transformation.market_transformer import (
    get_observed_at_from_object_name,
    transform_market_data,
)


logger = logging.getLogger("airflow.task")


@dag(
    dag_id="market_ingestion",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["market", "ingestion"],
)
def market_ingestion_dag():

    @task
    def ingest() -> str:
        object_name = ingest_market_data()

        logger.info(
            "Raw market data stored at: %s",
            object_name,
        )

        return object_name

    @task
    def transform(
        object_name: str,
    ) -> list[dict]:
        raw_data = read_json_object(object_name)

        observed_at = get_observed_at_from_object_name(
            object_name
        )

        transformed = transform_market_data(
            raw_data,
            observed_at,
        )

        logger.info(
            "Transformed %s market records",
            len(transformed),
        )

        return transformed

    @task
    def load(
        records: list[dict],
    ) -> int:
        inserted_count = load_market_records(records)

        logger.info(
            "Inserted %s new fact rows",
            inserted_count,
        )

        return inserted_count

    raw_object_name = ingest()

    transformed_records = transform(
        raw_object_name
    )

    load(transformed_records)


market_ingestion_dag()