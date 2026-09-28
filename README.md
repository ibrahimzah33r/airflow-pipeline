# Airflow Market Data Pipeline

A production-style ETL pipeline that extracts cryptocurrency market data from the Kraken API, stores immutable raw responses in MinIO, transforms and validates the data, and loads clean observations into PostgreSQL.

The pipeline is orchestrated by Apache Airflow and includes scheduling, retries, idempotent loading, data-quality checks, monitoring callbacks, automated tests, CI, and a small FastAPI read API.

## Architecture

```text
Kraken API
    |
    v
Apache Airflow
    |
    v
Ingestion
    |
    +----> MinIO
    |      Raw JSON
    |
    v
Transformation
    |
    v
Data Quality
    |
    v
PostgreSQL Warehouse
    |
    v
FastAPI
```

Airflow passes small values such as MinIO object paths between tasks using XCom. The raw dataset itself remains in object storage rather than being passed through Airflow's metadata database.

## Pipeline

The Airflow DAG runs hourly:

```text
ingest
   |
   v
transform
   |
   v
validate
   |
   v
load
```

### Extract

The ingestion layer retrieves BTC, ETH and SOL ticker data from Kraken's public API.

The untouched API response is stored in MinIO using timestamped object keys such as:

```text
raw/kraken/2026/09/28/140146.json
```

### Transform

Kraken-specific identifiers and response fields are converted into a stable internal representation.

The MinIO object timestamp is used as `observed_at`, ensuring that processing the same raw object multiple times produces the same logical observation.

### Validate

Before loading, records are checked for:

- required fields
- positive prices
- non-negative volume
- valid timestamps
- duplicate assets within a batch

Invalid data fails the Airflow task before reaching the warehouse.

### Load

Data is loaded into a PostgreSQL warehouse containing:

- `dim_asset`
- `fact_market_price`
- `daily_asset_summary`

The loader uses PostgreSQL conflict handling and the unique `(asset_id, observed_at)` constraint to provide idempotent loading.

Reprocessing the same raw snapshot therefore does not create duplicate fact rows.

## Reliability

The DAG includes:

- hourly scheduling
- task retries
- retry delays
- maximum one active DAG run
- idempotent database writes
- validation before loading
- DAG success/failure callbacks
- task retry callbacks

## FastAPI

A small API exposes warehouse data.

Start it with:

```bash
uvicorn api.main:app --reload
```

Endpoints:

```text
GET /health
GET /market/latest
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Technology Stack

- Python
- Apache Airflow
- PostgreSQL
- MinIO
- FastAPI
- Psycopg
- Docker Compose
- Pytest
- GitHub Actions

## Local Setup

Clone the repository and enter it:

```bash
git clone <repository-url>
cd airflow-pipeline
```

Create the environment file:

```bash
cp .env.example .env
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the infrastructure:

```bash
docker compose up -d
```

Airflow is available at:

```text
http://localhost:8080
```

MinIO Console:

```text
http://localhost:9001
```

FastAPI can be started separately with:

```bash
uvicorn api.main:app --reload
```

## Tests

Run unit tests:

```bash
./scripts/test-unit.sh
```

Run integration tests:

```bash
./scripts/test-integration.sh
```

The integration tests require the PostgreSQL warehouse container.

## Continuous Integration

GitHub Actions automatically:

1. starts PostgreSQL
2. creates the warehouse schema
3. installs the Python dependencies
4. runs unit tests
5. runs integration tests

CI runs on pushes and pull requests targeting `main`.

## Key Engineering Concepts Demonstrated

This project demonstrates:

- ETL pipeline design
- workflow orchestration
- DAGs and task dependencies
- object storage
- raw-data retention
- XCom-based task communication
- dimensional data modelling
- transformation boundaries
- data-quality validation
- idempotency
- retries and failure handling
- SQL joins and conflict handling
- dependency injection
- REST API development
- unit and integration testing
- Docker-based local infrastructure
- CI with GitHub Actions