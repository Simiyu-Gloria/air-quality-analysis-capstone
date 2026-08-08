# Data Acquisition: API Documentation

## Data source
**API:** OpenAQ v3 (`https://api.openaq.org/v3`)
**Authentication:** API key required, sent via the `X-API-Key` header (registered at explore.openaq.org)
**Client:** United Nations Environment Programme (UNEP)
**Cities studied:** Nairobi, Kampala, Kigali, Addis Ababa, Johannesburg, Lagos
**Study period:** 2021-01-01 to present (~5-year window, aligned with the brief's "most recent three to five years")

---

## Endpoints used

### 1. `GET /v3/locations`
**Purpose:** Identify monitoring stations within each city.

| Parameter | Value used | Notes |
|---|---|---|
| `coordinates` | `{lat},{lon}` per city center | e.g. Nairobi: `-1.286389,36.817223` |
| `radius` | `25000` (metres) | 25km — the maximum radius v3 allows for a single query |
| `limit` | `100` | Sufficient to capture all stations in every city studied; largest city (Lagos) returned 61 |

**Response used:** each location object includes an embedded `sensors` array listing every pollutant parameter that station measures, along with `datetimeFirst`/`datetimeLast` (station's reporting window) and `coordinates`. This meant a separate `/locations/{id}/sensors` call was unnecessary — sensor metadata is already present in the locations response.

**Stations found per city:** Nairobi 16, Kampala 36, Kigali 4, Addis Ababa 9, Johannesburg 12, Lagos 61.

---

### 2. `GET /v3/sensors/{sensor_id}/days`
**Purpose:** Pull daily-averaged PM2.5 measurements for each active sensor.

| Parameter | Value used | Notes |
|---|---|---|
| `date_from` | `2021-01-01` | Start of study window |
| `date_to` | current date | End of study window |
| `limit` | `1000` | Max page size |
| `page` | incremented until a page returns <1000 results | Pagination stop condition — the API's `meta.found` field returned inconsistent formats (plain integers, `"1000+"`, `">1000"`), so page-size was used as the reliable signal instead |

**Why daily averages instead of raw measurements:** the raw `/measurements` endpoint returns every individual reading (often hourly or sub-hourly), which would multiply request volume many times over for a 5-year window with limited added analytical value. Daily averages give sufficient resolution for trend, seasonal, and exceedance analysis while keeping the pull tractable within API rate limits.

---

## Preprocessing rules applied during acquisition (not just cleaning)

**Pollutant scope:** Measurement time-series was pulled for **PM2.5 only**. Other pollutants each station may monitor (PM10, SO2, NO2, O3, etc.) were catalogued by *frequency* (station counts per pollutant type, for Q2) but not pulled as full time-series. This is a deliberate scope decision: none of the six client questions require trend data for pollutants other than PM2.5, so pulling full history for them would add substantial API load without answering an assigned question.

**"Active sensor" definition:** A sensor is classified as active if its station's `datetimeLast.utc` falls within the 2 years prior to the pull date. Only active sensors had their measurement history pulled — sensors last reporting years ago (e.g. one Nairobi station last reported in 2018) were excluded from the measurement pull entirely, since a dead sensor cannot contribute to a "most recent 3-5 years" analysis. Inactive sensors are still recorded in `pm25_sensors_summary.json` for transparency in the QA section.

**Known limitation — Johannesburg:** 7 PM2.5 sensors were found, but only 1 was active by the above definition. Johannesburg's overall pollutant monitoring is also skewed toward SO2, PM10, and CO rather than PM2.5, likely reflecting industrial/regulatory-style monitoring infrastructure rather than the low-cost sensor networks (e.g. AirQo-affiliated stations) driving PM2.5 density in Kampala, Lagos, and Nairobi. Johannesburg was retained in the study rather than dropped, with this limitation documented rather than concealed — it can still answer "has PM2.5 changed over time" for the city, but not "which part of the city is worst," since only one station is available.

---

## Files produced

| File | Contents |
|---|---|
| `data/raw/{city}_locations.json` | Raw station metadata per city, as returned by `/v3/locations` |
| `data/raw/pm25_sensors_summary.json` | Extracted PM2.5 sensors across all cities, with active/inactive flag |
| `data/raw/{city}_measurements.json` | Daily-averaged PM2.5 readings per active sensor, per city |
| `data/raw/pollutant_frequency.csv` | Station counts per pollutant type per city (supports Q2) |
