from config import PipelineConfig,validate_env
from logger import get_logger
from ingest import fetch_employees,load_budgets
from transform import enrich_records,profile_transform,validate_records
from datetime import datetime
from exceptions import PipelineError
from load import save_report

def run_pipeline():
    config = PipelineConfig()
    validate_env(config)
    logger = get_logger("main", config.log_file)

    try:
        logger.info(f"Pipeline started : {datetime.now()}")

        employees = list(fetch_employees(config,logger))
        if not employees:
            raise PipelineError("The fetch employees function returned empty values")

        budgets = load_budgets(config,logger)
        if not budgets:
            raise PipelineError("The load budgets function returned empty values")

        valid_records = validate_records(employees,logger)
        if not valid_records:
            raise PipelineError("The validate records function returned empty values")

        enriched_records = enrich_records(valid_records,budgets,logger)
        if not enriched_records:
            raise PipelineError("The enrich records function returned empty values")

        df,summary_df = profile_transform(enriched_records,logger)
        if df.empty or summary_df.empty:
            raise PipelineError("The profile transform function returned empty values")

        save_report(df, config, logger)

    except PipelineError as e:
        logger.exception(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()