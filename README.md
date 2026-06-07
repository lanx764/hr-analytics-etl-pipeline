# HR Analytics ETL Pipeline

A modular, production-structured ETL pipeline that fetches employee data from 
the ReqRes API, enriches it with department budget data, validates and 
transforms records, and writes the final report to CSV.

---

## Project Structure

| File | Purpose |
|---|---|
| `config.py` | PipelineConfig class and validate_env function |
| `logger.py` | get_logger function with RotatingFileHandler |
| `exceptions.py` | Custom pipeline exceptions |
| `ingest.py` | fetch_employees and load_budgets functions |
| `transform.py` | validate_records, enrich_records, transform_records, profile_transform |
| `load.py` | save_report function |
| `pipeline.py` | run_pipeline orchestrator |
| `department_budgets.json` | Department budget reference data |

---

## What It Does

1. Loads and validates all environment variables via PipelineConfig
2. Fetches employee records from the ReqRes API across pages 1 and 2 using itertools.chain
3. Loads department budget data from a local JSON file
4. Validates records — rejects any with missing fields or invalid email
5. Enriches records — assigns departments and budget data to each employee
6. Transforms records — builds a Pandas DataFrame with vectorised operations
7. Profiles the transform stage using cProfile and pstats
8. Writes the final report to CSV

---

## Topics Integrated

Core Python, File Handling, Pandas, Datetime, JSON, Functions and Pipelines,
ETL/ELT Concepts, Reshaping, APIs, Error Handling, OOP, Environment Variables,
Logging, Writing Efficient Python

---

## How to Run

**Prerequisites:**
```bash
pip install pandas numpy requests python-dotenv memory-profiler
```

**Setup:**
1. Copy `.env.example` to `.env`
2. Add your ReqRes API key to `.env`

**Run:**
```bash
python pipeline.py
```

**Output:**
- `employee_report.csv` — final transformed employee data
- `pipeline.log` — full pipeline log with rotating file handlers

---

## Performance Considerations

**1. Most expensive operation at 1 million rows**
The `groupby` operation in `transform_records` would be the most expensive at scale because
Pandas has to scan all 1 million rows then group them by department and salary band,
then apply count and mean aggregations to each group which makes the dataset larger and
the more the dataset the more expensive the scan and grouping becomes.

**2. Why set conversion belongs outside the loop in enrich records**
In `enrich_records`, the budgets dict keys are converted to a set once before the
loop rather than inside it because If converted inside the loop, a new set would
be created on every single loop, paying the conversion cost repeatedly instead
of once. Converting once outside reduces the cost to O(1) per lookup.

**3. What breaks first at 10x data volume**
The `fetch_employees` function breaks first. It is hardcoded to fetch only pages
1 and 2. At 10x data volume the API would have more pages but the pipeline would
silently miss them.

---

## Pipeline Summary

This pipeline loads configuration from environment variables, validates that all
required variables are present, then fetches employee records from the ReqRes API
across two pages using itertools.chain to combine them. It then loads department
budget data from a local JSON file, validates each employee record by checking for
required fields and a valid email address and enriches each record by assigning
a department and its associated budget data using itertools.cycle.

The enriched records are loaded into a Pandas DataFrame where all transformations
are fully vectorised — no loops, no apply. New columns are added for full name,
email domain, salary, salary band, and ingestion date. The transform stage is
profiled using cProfile to surface any bottlenecks. The final DataFrame is written
to CSV and all pipeline activity is logged using a RotatingFileHandler.

Key decisions made: set lookup over list lookup for O(1) field validation,
itertools.chain to avoid building a combined list in memory, np.where over apply
for conditional column assignment, and modular file structure so each file has
one clear responsibility.
