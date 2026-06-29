"""Perhitungan backtesting harga saham setelah TOPSIS.

Membandingkan harga penutupan (Close) pada tanggal uji dengan harga
baseline 8 April 2025, lalu membuat peringkat gap terbesar ke terkecil.
"""

from dataclasses import dataclass

import pandas as pd

from dss_stock.audit_input import STOCK_VALUATION_DATE, get_historical_close_at_date
from dss_stock.constants import BACKTESTING_PERIODS, STOCK_NAMES


@dataclass
class BacktestingSteps:
    """Hasil backtesting per saham undervalued."""

    baseline_date: str
    baseline_prices: pd.DataFrame
    period_tables: dict[str, pd.DataFrame]
    combined_table: pd.DataFrame


def _rank_descending(values: dict[str, float]) -> dict[str, int]:
    ordered = sorted(values.items(), key=lambda item: item[1], reverse=True)
    return {code: index + 1 for index, (code, _) in enumerate(ordered)}


def calculate_backtesting_steps(stock_codes: list[str]) -> BacktestingSteps:
    """Hitung harga, gap, dan ranking backtesting untuk setiap periode."""
    baseline_ts = pd.Timestamp(STOCK_VALUATION_DATE)
    baseline_rows: list[dict[str, object]] = []

    for stock_code in stock_codes:
        symbol = f"{stock_code}.JK"
        price, actual_date = get_historical_close_at_date(symbol, baseline_ts)
        baseline_rows.append(
            {
                "kode": stock_code,
                "nama": STOCK_NAMES.get(stock_code, stock_code),
                "harga_baseline": price,
                "tanggal_baseline": actual_date.strftime("%Y-%m-%d"),
            }
        )

    baseline_df = pd.DataFrame(baseline_rows).set_index("kode")
    period_tables: dict[str, pd.DataFrame] = {}
    combined_rows: list[dict[str, object]] = []

    for stock_code in stock_codes:
        combined_rows.append(
            {
                "kode": stock_code,
                "nama": STOCK_NAMES.get(stock_code, stock_code),
                "harga_baseline": float(baseline_df.loc[stock_code, "harga_baseline"]),
            }
        )

    for period in BACKTESTING_PERIODS:
        end_ts = pd.Timestamp(period["endDate"])
        rows: list[dict[str, object]] = []
        gap_pct_by_code: dict[str, float] = {}

        for stock_code in stock_codes:
            symbol = f"{stock_code}.JK"
            baseline_price = float(baseline_df.loc[stock_code, "harga_baseline"])
            end_price, end_actual_date = get_historical_close_at_date(symbol, end_ts)
            gap_idr = end_price - baseline_price
            gap_pct = (end_price / baseline_price) - 1
            gap_pct_by_code[stock_code] = gap_pct

            rows.append(
                {
                    "kode": stock_code,
                    "nama": STOCK_NAMES.get(stock_code, stock_code),
                    "harga_baseline": baseline_price,
                    "harga_uji": end_price,
                    "tanggal_uji": end_actual_date.strftime("%Y-%m-%d"),
                    "gap_idr": gap_idr,
                    "gap_persen": gap_pct * 100,
                }
            )

        ranks = _rank_descending(gap_pct_by_code)
        for row in rows:
            row["rank"] = ranks[row["kode"]]

        period_df = (
            pd.DataFrame(rows)
            .sort_values("rank")
            .reset_index(drop=True)
        )
        period_tables[period["key"]] = period_df

        gap_col = f"gap_persen_{period['key']}"
        rank_col = period["key"]
        harga_col = f"harga_{period['endDate']}"
        gap_idr_col = f"gap_idr_{period['key']}"
        tanggal_col = (
            "tanggal_sep2025"
            if period["key"] == "rankApr2025vsSep2025"
            else "tanggal_apr2026"
        )
        for row in combined_rows:
            stock_code = row["kode"]
            period_row = period_df[period_df["kode"] == stock_code].iloc[0]
            row[harga_col] = float(period_row["harga_uji"])
            row[tanggal_col] = period_row["tanggal_uji"]
            row[gap_idr_col] = float(period_row["gap_idr"])
            row[gap_col] = float(period_row["gap_persen"])
            row[rank_col] = int(period_row["rank"])

    combined_table = pd.DataFrame(combined_rows).sort_values(
        "rankApr2025vsSep2025"
    ).reset_index(drop=True)

    return BacktestingSteps(
        baseline_date=STOCK_VALUATION_DATE,
        baseline_prices=baseline_df,
        period_tables=period_tables,
        combined_table=combined_table,
    )


def backtesting_to_api_dict(steps: BacktestingSteps) -> dict[str, dict[str, float | int]]:
    """Konversi hasil backtesting ke format yang dipakai API."""
    results: dict[str, dict[str, float | int]] = {}
    for stock_code in steps.baseline_prices.index:
        row = steps.combined_table[steps.combined_table["kode"] == stock_code].iloc[0]
        results[stock_code] = {
            "nama": STOCK_NAMES.get(stock_code, stock_code),
            "hargaBaseline": float(row["harga_baseline"]),
            "hargaSep2025": float(row["harga_2025-09-01"]),
            "hargaApr2026": float(row["harga_2026-04-01"]),
            "returnApr2025vsSep2025": float(row["gap_persen_rankApr2025vsSep2025"]) / 100,
            "returnApr2025vsApr2026": float(row["gap_persen_rankApr2025vsApr2026"]) / 100,
            "rankApr2025vsSep2025": int(row["rankApr2025vsSep2025"]),
            "rankApr2025vsApr2026": int(row["rankApr2025vsApr2026"]),
        }
    return results
