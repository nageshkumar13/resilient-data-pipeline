import logging
from pathlib import Path


def setup_logger(log_path: Path) -> logging.Logger:
    """Create and return a simple file logger for the pipeline."""

    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("resilient_data_pipeline")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
