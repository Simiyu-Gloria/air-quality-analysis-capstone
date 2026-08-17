import json
import os
from datetime import datetime, timezone, timedelta

CITIES = ["nairobi", "kampala", "kigali", "addis_ababa", "johannesburg", "lagos"]

# How recent a station's last reading must be to count as "active" for our
# study window. Brief suggests most recent 3-5 years - we use 2 years as the
# active cutoff so stations that went quiet recently still get flagged, not
# silently dropped.
RECENCY_CUTOFF = datetime.now(timezone.utc) - timedelta(days=2 * 365)


def extract_pm25_sensors(city):
    path = f"data/raw/{city}_locations.json"
    with open(path) as f:
        data = json.load(f)

    rows = []
    for loc in data["results"]:
        for sensor in loc.get("sensors", []):
            if sensor["parameter"]["name"] != "pm25":
                continue

            last_str = loc.get("datetimeLast", {}).get("utc")
            last_dt = datetime.fromisoformat(last_str.replace("Z", "+00:00")) if last_str else None
            is_active = last_dt is not None and last_dt >= RECENCY_CUTOFF

            rows.append({
                "city": city,
                "station_id": loc["id"],
                "station_name": loc["name"],
                "sensor_id": sensor["id"],
                "provider": loc.get("provider", {}).get("name"),
                "datetime_first": loc.get("datetimeFirst", {}).get("utc"),
                "datetime_last": last_str,
                "is_active": is_active,
                "latitude": loc["coordinates"]["latitude"],
                "longitude": loc["coordinates"]["longitude"],
            })
    return rows


def main():
    all_rows = []
    for city in CITIES:
        rows = extract_pm25_sensors(city)
        active = sum(r["is_active"] for r in rows)
        print(f"{city}: {len(rows)} pm25 sensor(s) found, {active} active (reported within last 2 years)")
        all_rows.extend(rows)

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/pm25_sensors_summary.json", "w") as f:
        json.dump(all_rows, f, indent=2)

    print("\nSaved data/raw/pm25_sensors_summary.json")
    print("Review this before Step 3 - inactive sensors should probably be excluded from the measurement pull.")


if __name__ == "__main__":
    main()
