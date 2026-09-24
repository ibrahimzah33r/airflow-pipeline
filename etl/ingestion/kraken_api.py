import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv(".env")


def fetch_market_data() -> dict[str, Any]:
    api_url = os.environ["KRAKEN_API_URL"]

    pairs = os.getenv(
        "KRAKEN_PAIRS",
        "XBTUSD,ETHUSD,SOLUSD",
    )

    response = requests.get(
        api_url,
        params={"pair": pairs},
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    errors = data.get("error", [])

    if errors:
        raise RuntimeError(
            f"Kraken API returned errors: {errors}"
        )

    result = data.get("result")

    if not isinstance(result, dict) or not result:
        raise ValueError(
            "Kraken API response did not contain market data"
        )

    return data