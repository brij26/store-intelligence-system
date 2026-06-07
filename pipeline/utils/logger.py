import logging
from pathlib import Path


def setup_logger(name: str):

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(
        log_dir / "pipeline.log"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger