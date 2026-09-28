from datetime import datetime, timezone
from typing import Any


ASSET_MAP = {
    "XXBTZUSD": {
        "external_id": "bitcoin",
        "symbol": "BTC",
        "name": "Bitcoin",
    },
    "XETHZUSD": {
        "external_id": "ethereum",
        "symbol": "ETH",
        "name": "Ethereum",
    },
    "SOLUSD": {
        "external_id": "solana",
        "symbol": "SOL",
        "name": "Solana",
    },
}


def get_observed_at_from_object_name(
    object_name: str,
) -> datetime:
    path = object_name.removesuffix(".json")

    timestamp_text = path.split("raw/kraken/")[1]

    return datetime.strptime(
        timestamp_text,
        "%Y/%m/%d/%H%M%S",
    ).replace(tzinfo=timezone.utc)


def transform_market_data(
    raw_data: dict[str, Any],
    observed_at: datetime,
) -> list[dict[str, Any]]:
    result = raw_data.get("result")

    if not isinstance(result, dict) or not result:
        raise ValueError(
            "Kraken response contains no market data"
        )

    transformed: list[dict[str, Any]] = []

    for pair_name, ticker in result.items():
        asset = ASSET_MAP.get(pair_name)

        if asset is None:
            continue

        last_trade_price = float(ticker["c"][0])
        volume_24h = float(ticker["v"][1])

        volume_24h_usd = (
            volume_24h * last_trade_price
        )

        transformed.append(
            {
                **asset,
                "observed_at": observed_at.isoformat(),
                "price_usd": last_trade_price,
                "volume_24h_usd": volume_24h_usd,
            }
        )

    if not transformed:
        raise ValueError(
            "No supported Kraken assets were found"
        )

    return transformed