from exceptions import PipelineError

def save_report(df,config,logger):
    try:
        df.to_csv(config.output_file,index=False)
        df_rows = len(df)
        logger.info(f"{df_rows} rows were written to {config.output_file}")
    except OSError as e:
        raise PipelineError(f"Writing of the dataframe to {config.output_file} failed: {e}")
