"""Prüft den laufenden Azure-Stand gegen den Commit des Deployment-Jobs."""

import json
import os
import time
from urllib.error import URLError
from urllib.request import urlopen


def verify_deployment(url, expected_commit, attempts=12, delay=10):
    for attempt in range(attempts):
        try:
            with urlopen(url.rstrip("/") + "/health", timeout=20) as response:
                data = json.load(response)
            if data.get("status") == "ok" and data.get("commit") == expected_commit:
                return data
        except (URLError, TimeoutError, json.JSONDecodeError):
            pass
        if attempt + 1 < attempts:
            time.sleep(delay)
    raise RuntimeError("Azure-App antwortet nicht mit der erwarteten Release-Version.")


if __name__ == "__main__":
    result = verify_deployment(os.environ["APP_URL"], os.environ["EXPECTED_SHA"])
    print(f"Auslieferung über HTTP bestätigt: {result['commit']}")
