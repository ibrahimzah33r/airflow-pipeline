import logging
from typing import Any


logger = logging.getLogger("airflow.task")


def dag_success_callback(
    context: dict[str, Any],
) -> None:
    logger.info(
        "PIPELINE SUCCESS | dag=%s | run_id=%s",
        context["dag"].dag_id,
        context["run_id"],
    )


def dag_failure_callback(
    context: dict[str, Any],
) -> None:
    task_instance = context.get("task_instance")
    exception = context.get("exception")

    task_id = (
        task_instance.task_id
        if task_instance
        else "unknown"
    )

    logger.error(
        "PIPELINE FAILURE | dag=%s | run_id=%s | "
        "task=%s | error=%s",
        context["dag"].dag_id,
        context["run_id"],
        task_id,
        exception,
    )


def task_retry_callback(
    context: dict[str, Any],
) -> None:
    task_instance = context["task_instance"]

    logger.warning(
        "TASK RETRY | dag=%s | task=%s | "
        "run_id=%s | try=%s",
        context["dag"].dag_id,
        task_instance.task_id,
        context["run_id"],
        task_instance.try_number,
    )