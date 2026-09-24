# Airflow Pipeline

A production-style ETL data pipeline built with Apache Airflow.

The pipeline will:

1. Extract market data from a public API.
2. Store raw API responses in MinIO.
3. Clean and transform the data.
4. Load processed data into PostgreSQL.
5. Run automatically with Apache Airflow.
6. Include retries, logging, monitoring, and data-quality checks.

## Architecture

Public API → Airflow → MinIO → Transformation → PostgreSQL

## Status

Under active development.
# airflow-pipeline
