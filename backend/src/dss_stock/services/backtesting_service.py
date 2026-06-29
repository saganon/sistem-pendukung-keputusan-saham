"""Wrapper backtesting untuk layanan API."""

from dss_stock.calculate_backtesting import (
    BacktestingSteps,
    backtesting_to_api_dict,
    calculate_backtesting_steps,
)

_last_backtesting_steps: BacktestingSteps | None = None


def run_backtesting(stock_codes: list[str]) -> BacktestingSteps:
    global _last_backtesting_steps
    _last_backtesting_steps = calculate_backtesting_steps(stock_codes)
    return _last_backtesting_steps


def get_backtesting_steps() -> BacktestingSteps | None:
    return _last_backtesting_steps


def calculate_backtesting_ranks(
    stock_codes: list[str],
) -> dict[str, dict[str, float | int]]:
    """Hitung return dan ranking backtesting per periode."""
    steps = run_backtesting(stock_codes)
    return backtesting_to_api_dict(steps)
