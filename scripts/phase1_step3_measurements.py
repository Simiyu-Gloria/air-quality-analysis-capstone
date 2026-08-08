"""
Phase 1 - Step 3: Pull daily-averaged PM2.5 measurements for every ACTIVE
sensor identified in Step 2 (pm25_sensors_summary.json).

WHY "active" sensors only:
Step 2 flagged each sensor as active/inactive based on whether its station
reported within the last 2 years. Dead sensors would just return empty
pages here and waste API calls/rate-limit budget for no benefit.

WHY daily averages, not raw measurements:
OpenAQ's raw /measurements endpoint returns every individual reading
(often hourly or sub-hourly). For a ~5-year study window across ~120
sensors, that's a huge number of API calls for resolution we don't need.
The /days endpoint gives one pre-averaged value per day per sensor, which
is enough detail for trend, seasonal, and WHO-exceedance analysis while
keeping the total pull tractable.

RESUME SAFETY:
This script can safely be re-run if it crashes partway through (e.g. a
network blip, or a new API quirk we haven't seen yet). It checks whether
a city's output file already exists before pulling that city again, so
you never lose completed work or double-pull a city that's already done.
If you genuinely want to re-pull a city from scratch, delete its
data/raw/{city}_measurements.json file first.
"""

import os
import json
import time
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()  # reads OPENAQ_API_KEY from a .env file in the current directory

API_KEY = os.environ["OPENAQ_API_KEY"]
BASE_URL = "https://api.openaq.org/v3"
HEADERS = {"X-API-Key": API_KEY}

# Study window: matches the brief's "most recent three to five years" guidance.
DATE_FROM = "2021-01-01"
DATE_TO = date.today().isoformat()

# Pause between API calls to stay comfortably under OpenAQ's rate limit.
# If you see repeated "rate limited" messages, increase this value.
SLEEP_BETWEEN_CALLS = 1.2


def fetch_daily_averages(sensor_id):
    """
    Pull every page of daily-averaged measurements for one sensor.

    OpenAQ paginates results in blocks of up to `limit` (we use 1000).
    We keep requesting pages until a page comes back with FEWER than
    1000 results - that's the reliable signal that we've reached the
    last page.

    NOTE: We deliberately do NOT rely on the API's `meta.found` field to
    decide when to stop. In practice it came back in several different
    formats across different sensors/requests ("1000+", ">1000", or a
    plain number), and parsing it as a stopping condition caused crashes.
    Page-size is a simpler and more robust signal that doesn't depend on
    OpenAQ's response format being consistent.
    """
    all_days = []
    page = 1

    while True:
        url = f"{BASE_URL}/sensors/{sensor_id}/days"
        params = {
            "date_from": DATE_FROM,
            "date_to": DATE_TO,
            "limit": 1000,
            "page": page,
        }
        resp = requests.get(url, headers=HEADERS, params=params)

        # OpenAQ returns 429 if we're calling too fast. Back off and retry
        # rather than crashing - this can happen even with our sleep delay
        # if the API is under load.
        if resp.status_code == 429:
            print(f"    rate limited on sensor {sensor_id}, page {page} - waiting 30s")
            time.sleep(30)
            continue

        resp.raise_for_status()  # raises an error for any other bad status (4xx/5xx)
        data = resp.json()
        results = data.get("results", [])
        all_days.extend(results)

        if len(results) < 1000:
            break  # short page = this was the last page

        page += 1
        time.sleep(SLEEP_BETWEEN_CALLS)

    return all_days


def main():
    # Step 2's output: every PM2.5 sensor across all 6 cities, with an
    # is_active flag already computed.
    with open("data/raw/pm25_sensors_summary.json") as f:
        sensors = json.load(f)

    active_sensors = [s for s in sensors if s["is_active"]]
    print(f"Pulling measurements for {len(active_sensors)} active sensors "
          f"(skipping {len(sensors) - len(active_sensors)} inactive)\n")

    # Group sensors by city so we can save one output file per city.
    by_city = {}
    for s in active_sensors:
        by_city.setdefault(s["city"], []).append(s)

    for city, city_sensors in by_city.items():
        out_path = f"data/raw/{city}_measurements.json"

        # Resume safety: skip cities we've already completed in a prior run.
        if os.path.exists(out_path):
            print(f"{city}: already done (found {out_path}) - skipping\n")
            continue

        city_data = []
        for s in city_sensors:
            print(f"{city}: sensor {s['sensor_id']} ({s['station_name']})")
            days = fetch_daily_averages(s["sensor_id"])
            city_data.append({
                "station_id": s["station_id"],
                "station_name": s["station_name"],
                "sensor_id": s["sensor_id"],
                "latitude": s["latitude"],
                "longitude": s["longitude"],
                "daily_averages": days,
            })
            print(f"    -> {len(days)} daily records")
            time.sleep(SLEEP_BETWEEN_CALLS)

        with open(out_path, "w") as f:
            json.dump(city_data, f, indent=2)
        print(f"Saved {out_path}\n")

    print("Done. All measurement data is in data/raw/*_measurements.json")


if __name__ == "__main__":
    main()