import pandas as pd
from pathlib import Path

try:
    from cleaner import clean_users
    from loader import load_csv
    from logger_config import setup_logger
except ModuleNotFoundError:
    from src.cleaner import clean_users
    from src.loader import load_csv
    from src.logger_config import setup_logger

# Paths used by the pipeline
project_root = Path(__file__).parent.parent
raw_path = project_root / "data" / "raw" / "global_user.csv"
processed_path = project_root / "data" / "processed" / "processed_users.csv"
rejected_path = project_root / "data" / "rejected" / "rejected_users.csv"
report_path = project_root / "reports" / "inspection_report.txt"
log_path = project_root / "logs" / "pipeline.log"


def build_report_text(report: dict[str, int]) -> str:
    """Build a simple human-readable pipeline report."""
    return f"""========== ETL REPORT ==========

Input Rows: {report['input_row_count']}

Valid Email Rows: {report['valid_email_rows_before_duplicates']}
Final Processed Rows: {report['processed_row_count']}

Invalid Email Rows: {report['invalid_email_count']}
Rejected Duplicate Rows: {report['duplicate_rejected_count']}

Total Rejected Rows: {report['rejected_row_count']}

Processed File:
{processed_path.relative_to(project_root)}

Rejected File:
{rejected_path.relative_to(project_root)}

================================
"""


def main() -> None:
    logger = setup_logger(log_path)
    logger.info("Pipeline started")

    try:
        # 1. Load CSV
        df = load_csv(raw_path)
        logger.info(f"CSV loaded successfully from {raw_path}")

        # 2. Run validation and cleaning
        processed_df, rejected_df, report = clean_users(df)
        logger.info("Data cleaning completed")

        # 3. Save processed and rejected files
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        rejected_path.parent.mkdir(parents=True, exist_ok=True)
        processed_df.to_csv(processed_path, index=False)
        rejected_df.to_csv(rejected_path, index=False)
        logger.info(f"Processed file saved to {processed_path}")
        logger.info(f"Rejected file saved to {rejected_path}")

        # 4. Save and print report
        report_text = build_report_text(report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")
        print(f"\n{report_text}")
        print(f"Inspection Report: {report_path}")
        logger.info(f"Inspection report saved to {report_path}")
        logger.info("Pipeline finished successfully")

    except FileNotFoundError:
        logger.error(f"File not found: {raw_path}")
        print(f"Error: File not found at {raw_path}")
    except pd.errors.EmptyDataError:
        logger.error(f"CSV file is empty: {raw_path}")
        print(f"Error: CSV file is empty at {raw_path}")
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        print(f"Error running pipeline: {e}")


if __name__ == "__main__":
    main()
