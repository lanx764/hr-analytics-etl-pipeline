import pandas as pd
import itertools
import numpy as np
from datetime import date
import cProfile
import pstats

def validate_records(all_records,logger):
    required_fields = {"id", "email", "first_name", "last_name"}

    valid_records = []

    for record in all_records:
        missing_fields = required_fields.difference(record.keys())

        if missing_fields:
            logger.warning(f"The record with id : {record["id"]} was rejected due to missing fields: {missing_fields}")
            continue

        if "@" not in record["email"]:
            logger.warning(f"The record with id : {record["id"]} was rejected due to invalid email which doesnt have '@': {record['email']}")
            continue

        valid_records.append(record)

    return valid_records

def enrich_records(valid_records,budgets,logger):
    budget_keys = set(budgets.keys())
    department_names = list(budgets.keys())
    cycled_departments = itertools.cycle(department_names)

    enriched_records = []

    for record in valid_records:
        department = next(cycled_departments)

        record["department"] = department

        if department not in budget_keys:
            logger.warning(f"{department} not found in {budget_keys}")
            continue

        record["budget"] = budgets[department]["budget"]
        record["headcount_limit"] = budgets[department]["headcount_limit"]

        enriched_records.append(record)

    return enriched_records

def transform_records(enriched_records,logger):
    df = pd.DataFrame(enriched_records)
    before = len(df)

    df["full_name"] = df["first_name"] + " " + df["last_name"]
    df["email_domain"] = df["email"].str.split("@").str[1]
    df["salary"] = (df["budget"] / df["headcount_limit"]).round(2)
    df["salary_band"] = np.where(df["salary"] > 50000, "senior", "junior")
    df["ingestion_date"] = date.today().strftime("%Y-%m-%d")

    after = len(df)

    summary_df = df.groupby(["department","salary_band"]).agg(
        employee_count=("full_name","count"),
        average_salary=("salary","mean")).reset_index()

    logger.info(f"{before} records were entered and the final dataframe consists of {after}")

    return df,summary_df

def profile_transform(enriched_records,logger):
    profiler = cProfile.Profile()
    profiler.enable()

    df,summary_df = transform_records(enriched_records,logger)

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumtime")
    stats.print_stats(5)

    transformed = df,summary_df
    return transformed