"""
Answers Q2: "Which pollutants are monitored most frequently across the
selected cities?"

Reads the ORIGINAL Step 1 locations files (not the PM2.5-filtered Step 2
output) since we need every pollutant type each station monitors, not just
PM2.5. No new API calls needed - this is all local extraction.
"""

import json
import csv

CITIES = ["nairobi", "kampala", "kigali", "addis_ababa", "johannesburg", "lagos"]


def count_pollutants(city):
    with open(f"data/raw/{city}_locations.json") as f:
        data = json.load(f)

    counts = {}
    for loc in data["results"]:
        for sensor in loc.get("sensors", []):
            param = sensor["parameter"]["displayName"]
            counts[param] = counts.get(param, 0) + 1
    return counts


def main():
    all_counts = {}
    for city in CITIES:
        counts = count_pollutants(city)
        all_counts[city] = counts
        ranked = sorted(counts.items(), key=lambda x: -x[1])
        summary = ", ".join(f"{name} ({n})" for name, n in ranked)
        print(f"{city}: {summary}")

    # Build a tidy CSV: one row per city x pollutant, ready for a chart
    all_pollutants = sorted({p for c in all_counts.values() for p in c})
    with open("data/raw/pollutant_frequency.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["city", "pollutant", "station_count"])
        for city, counts in all_counts.items():
            for pollutant in all_pollutants:
                writer.writerow([city, pollutant, counts.get(pollutant, 0)])

    print("\nSaved data/raw/pollutant_frequency.csv")


if __name__ == "__main__":
    main()