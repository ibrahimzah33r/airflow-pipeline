from datetime import datetime
from typing import Any


REQUIRED_FIELDS = {
    "external_id",
    "symbol",
    "name",
    "observed_at",
    "price_usd",
    "volume_24h_usd",
}


def validate_market_records(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not records:
        raise ValueError("No market records to validate")

    seen_assets: set[str] = set()

    for record in records:
        missing_fields = REQUIRED_FIELDS - record.keys()

        if missing_fields:
            raise ValueError(
                f"Missing required fields: {sorted(missing_fields)}"
            )

        external_id = record["external_id"]

        if external_id in seen_assets:
            raise ValueError(
                f"Duplicate asset in batch: {external_id}"
            )

        seen_assets.add(external_id)

        if record["price_usd"] <= 0:
            raise ValueError(
                f"Invalid price for {external_id}: "
                f"{record['price_usd']}"
            )

        if record["volume_24h_usd"] < 0:
            raise ValueError(
                f"Invalid volume for {external_id}: "
                f"{record['volume_24h_usd']}"
            )

        try:
            datetime.fromisoformat(
                record["observed_at"]
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Invalid observed_at for {external_id}"
            ) from exc

    return records