from collections.abc import Generator

import psycopg

from etl.loading.warehouse_loader import get_warehouse_connection


def get_db() -> Generator[psycopg.Connection, None, None]:
    connection = get_warehouse_connection()

    try:
        yield connection
    finally:
        connection.close()