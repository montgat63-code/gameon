"""Structured diagnostics for the application shell."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(log_directory: str | Path) -> logging.Logger:
    directory = Path(log_directory)
    directory.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("gamemaster")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(directory / "gamemaster.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
    return logger


def summarize_failure(component: str, error: BaseException) -> str:
    return f"{component}: {type(error).__name__}: {error}"
