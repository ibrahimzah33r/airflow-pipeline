import logging

import pendulum
from airflow.sdk import dag, task

from etl.ingestion.market_ingestion import ingest_market_data


logger = logging.getLogger("airflow.task")


@dag(
    dag_id="market_ingestion",
    schedule=None,
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="UTC",
    ),
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

    ingest()


market_ingestion_dag()