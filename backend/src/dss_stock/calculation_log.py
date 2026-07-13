"""Helper logging untuk jejak perhitungan Entropy & TOPSIS."""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger("dss_stock.calculation")

_FLOAT_FMT = "{:.6f}"


def configure_calculation_logging(level: int = logging.INFO) -> None:
    """Pastikan logger perhitungan tampil di console."""
    if logger.handlers:
        logger.setLevel(level)
        return

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False


def log_section(title: str) -> None:
    border = "=" * 72
    logger.info(border)
    logger.info(title)
    logger.info(border)


def log_step(step: int, title: str, formula: str) -> None:
    logger.info("")
    logger.info("--- Langkah %s: %s ---", step, title)
    logger.info("Rumus: %s", formula)


def log_text(message: str) -> None:
    logger.info(message)


def log_dataframe(label: str, df: pd.DataFrame) -> None:
    logger.info("%s:", label)
    for line in df.to_string(float_format=lambda v: _FLOAT_FMT.format(v)).splitlines():
        logger.info("  %s", line)


def log_series(label: str, series: pd.Series) -> None:
    logger.info("%s:", label)
    for key, value in series.items():
        logger.info("  %s = %s", key, _FLOAT_FMT.format(float(value)))


def fmt(value: float) -> str:
    return _FLOAT_FMT.format(float(value))
