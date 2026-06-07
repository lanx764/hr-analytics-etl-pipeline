import itertools
import requests
import json
from exceptions import APIError, PipelineError

def fetch_employees(config, logger):
    try:
        response1 = requests.get(config.api_url, headers={"x-api-key": config.api_key}, params={"page": 1})
        response1.raise_for_status()
        page1_records = response1.json()["data"]
        logger.info(f"Page 1 returned {len(page1_records)} records")

        response2 = requests.get(config.api_url, headers={"x-api-key": config.api_key}, params={"page": 2})
        response2.raise_for_status()
        page2_records = response2.json()["data"]
        logger.info(f"Page 2 returned {len(page2_records)} records")

    except requests.RequestException as e:
        raise APIError(f"Failed to fetch employees due to: {e}")

    all_records = itertools.chain(page1_records, page2_records)
    return all_records

def load_budgets(config, logger):
    try:
        with open(config.budget_file, "r") as f:
            budgets = json.load(f)
        logger.info(f"Successfully loaded budgets from {config.budget_file}")
        return budgets
    except FileNotFoundError:
        raise PipelineError(f"Budget file not found at path: {config.budget_file}")
    except json.decoder.JSONDecodeError as e:
        raise PipelineError(f"Budget file is malformed : {e}")
