# Air Quality Patterns in African Cities

Data Analytics and Visualization Capstone (Group 5)

## Project Context

UNEP commissioned this analysis to investigate air quality patterns across selected African cities and support evidence-based intervention planning.

- Client: United Nations Environment Programme (UNEP)
- API: OpenAQ v3
- Cities: Nairobi, Kampala, Kigali, Addis Ababa, Johannesburg, Lagos
- Study window: 2021 to present (most recent 3 to 5 years)

## Repository Structure

```text
air-quality-analysis-capstone/
├── dashboard/
│   ├── air_quality_dashboard.pbix
│   └── air_quality_dashboard.pdf
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── visualizaion/
├── notebooks/
│   ├── analysis.ipynb
│   └── Phase1_API_Documentation.md
├── scripts/
│   ├── phase1_step1_locations.py
│   ├── phase1_step2_extract_sensors.py
│   ├── phase1_step3_measurements.py
│   └── pollutant_frequency.py
├── slides/
│   └── air_quality_capstone_deck.pptx
└── README.md
```

## Project Expectations Coverage

1. API retrieval and documentation
	- Implemented in `scripts/phase1_step1_locations.py`, `scripts/phase1_step3_measurements.py`
	- Documented in `notebooks/Phase1_API_Documentation.md` and Notebook Section 1
2. Data quality assessment (missingness, duplicates, outliers, completeness, consistency)
	- Implemented in Notebook Section 3 (`notebooks/analysis.ipynb`)
3. Data cleaning and preparation decisions
	- Implemented and explained in Notebook Section 4
	- Output: `data/cleaned/air_quality_master.csv`
4. EDA + at least three statistical techniques
	- Implemented in Notebook Section 5
	- Includes statistical analysis supporting all six research questions
5. At least five meaningful visualizations with justification
	- Implemented in Notebook Section 6
	- Exported charts in `data/visualizaion/` (6 PNG charts)
6. Interactive dashboard (KPIs, interactive charts, filters, map, executive summary, drill-down where possible)
	- Delivered in `dashboard/air_quality_dashboard.pbix`
7. Evidence-based findings and recommendations
	- Included in Notebook narrative and conclusion sections
8. Group contribution documentation and oral defense readiness
	- Documented in the Member Contributions section below
9. GitHub repository maintenance
	- Requirement satisfied by this repository

## How to Reproduce the Analysis

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install pandas numpy scipy matplotlib requests python-dotenv
```

3. Add `.env` file with OpenAQ key:

```env
OPENAQ_API_KEY=your_api_key_here
```

4. Run acquisition scripts (from repo root):

```bash
python scripts/phase1_step1_locations.py
python scripts/phase1_step2_extract_sensors.py
python scripts/phase1_step3_measurements.py
python scripts/pollutant_frequency.py
```

5. Open and run `notebooks/analysis.ipynb` to reproduce QA, cleaning, EDA, and visualizations.

## Notes and Constraints

- PM2.5 was used for full time-series analysis to match the core intervention questions.
- Other pollutants are analyzed for monitoring-frequency comparison (Q2).
- Johannesburg has relatively low active PM2.5 sensor coverage, documented as a data limitation.

## Team

Group 5 (Air Quality Patterns in African Cities).

## Member Contributions

The team followed a phased implementation plan with clear ownership per workstream.

- Samuel Tokoye
	- Phase 1 lead: API data acquisition workflow and raw JSON pulls
	- Phase 7 lead: findings and recommendations synthesis for UNEP
	- Phase 8 co-owner: repository packaging and README finalization
- Paul Kibet Miningwa
	- Phase 4 lead: EDA and statistical analysis for the six client questions
	- Contributed statistical interpretation for evidence-based conclusions
- Winnie Odoyo
	- Phase 3 lead: data cleaning and preprocessing into the master cleaned CSV
	- Phase 6 lead: interactive Power BI dashboard development
	- Phase 8 co-owner: presentation slide finalization
- Gloria Simiyu Wandabwa
	- Phase 0 lead: repository setup, project structure, and collaboration onboarding
	- Phase 2 lead: data quality assessment (missingness, duplicates, outliers, completeness, consistency)
	- Phase 5 lead: visualization design and chart production

Shared team responsibilities:

- API key registration, scope confirmation, and phase role assignment
- Final video and slides preparation and participation by all group members
