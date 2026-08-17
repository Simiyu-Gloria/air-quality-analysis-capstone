"""
Phase 1 - Step 1: Find OpenAQ monitoring stations for each city.

Run this first, in isolation, to see what stations actually exist
before writing anything about sensors or measurements.
"""

import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()  # reads .env in the current working directory

API_KEY = os.environ["OPENAQ_API_KEY"]
BASE_URL = "https://api.openaq.org/v3"
HEADERS = {"X-API-Key": API_KEY}

# Approx city centers. radius is in metres (25000 = 25km, the v3 max).
CITIES = {
    "nairobi":      {"lat": -1.286389, "lon": 36.817223},
    "kampala":      {"lat": 0.347596,  "lon": 32.582520},
    "kigali":       {"lat": -1.944072, "lon": 30.061885},
    "addis_ababa":  {"lat": 9.024680,  "lon": 38.746799},
    "johannesburg": {"lat": -26.204103, "lon": 28.047305},
    "lagos":        {"lat": 6.524379,  "lon": 3.379206},
}

RADIUS_M = 25000  # 25km search radius around each city center


def get_locations_for_city(city_name, lat, lon):
    url = f"{BASE_URL}/locations"
    params = {
        "coordinates": f"{lat},{lon}",
        "radius": RADIUS_M,
        "limit": 100,
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()
    print(f"{city_name}: found {data['meta']['found']} location(s)")
    return data


def main():
    os.makedirs("data/raw", exist_ok=True)
    all_results = {}

    for city, coords in CITIES.items():
        data = get_locations_for_city(city, coords["lat"], coords["lon"])
        all_results[city] = data
        # save raw response immediately, per city
        with open(f"data/raw/{city}_locations.json", "w") as f:
            json.dump(data, f, indent=2)
        time.sleep(1)  # be polite to the rate limit

    print("\nDone. Check data/raw/*_locations.json")


if __name__ == "__main__":
    main()
