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
- `pipeline.log` — full pipeline log with rotating file handler