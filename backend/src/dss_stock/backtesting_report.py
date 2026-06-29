"""Cetak tabel hasil backtesting penelitian."""

import pandas as pd

from dss_stock.calculate_backtesting import BacktestingSteps, calculate_backtesting_steps
from dss_stock.constants import BACKTESTING_PERIODS

BACKTESTING_FORMULAS = {
    "harga_baseline": "Harga penutupan (Close) pada 8 April 2025 — acuan keputusan TOPSIS",
    "harga_uji": "Harga penutupan (Close) pada tanggal uji backtesting",
    "gap_idr": "Gap (Rp) = Harga Uji − Harga Baseline",
    "gap_persen": "Gap (%) = (Harga Uji / Harga Baseline − 1) × 100",
    "rank": "Peringkat berdasarkan gap (%) terbesar ke terkecil (rank 1 = kenaikan tertinggi)",
}


def run_backtesting_analysis(stock_codes: list[str]) -> BacktestingSteps:
    return calculate_backtesting_steps(stock_codes)


def print_backtesting_tables(steps: BacktestingSteps) -> None:
    pd.options.display.float_format = "{:,.2f}".format
    pd.options.display.max_columns = None
    pd.options.display.width = None

    print("\n=== BACKTESTING — Uji Validitas Penelitian ===")
    print(
        "Membandingkan harga saham undervalued (hasil TOPSIS) dengan harga "
        f"baseline {steps.baseline_date}."
    )

    print("\n--- Rumus Backtesting ---")
    for step_name, formula in BACKTESTING_FORMULAS.items():
        print(f"  {step_name}: {formula}")

    print("\n--- Harga Baseline (Acuan Keputusan) ---")
    baseline_display = steps.baseline_prices.reset_index()[
        ["kode", "nama", "harga_baseline", "tanggal_baseline"]
    ].rename(
        columns={
            "harga_baseline": "harga_8_apr_2025",
            "tanggal_baseline": "tanggal_aktual",
        }
    )
    print(baseline_display.to_string(index=False))

    for period in BACKTESTING_PERIODS:
        period_df = steps.period_tables[period["key"]]
        end_label = period["endDate"]

        print(f"\n--- Periode: {period['label']} (harga uji target: {end_label}) ---")
        display_df = period_df[
            [
                "kode",
                "nama",
                "harga_baseline",
                "harga_uji",
                "tanggal_uji",
                "gap_idr",
                "gap_persen",
                "rank",
            ]
        ].rename(
            columns={
                "harga_baseline": "harga_8_apr_2025",
                "harga_uji": f"harga_{end_label}",
                "tanggal_uji": "tanggal_aktual",
                "gap_idr": "gap_rp",
                "gap_persen": "gap_persen",
                "rank": period["key"],
            }
        )
        print(display_df.to_string(index=False))

    print("\n--- Tabel Gabungan Backtesting (Semua Periode) ---")
    combined = steps.combined_table.copy()
    combined = combined.rename(
        columns={
            "harga_baseline": "harga_8_apr_2025",
            "harga_2025-09-01": "harga_1_sep_2025",
            "gap_idr_rankApr2025vsSep2025": "gap_rp_sep2025",
            "gap_persen_rankApr2025vsSep2025": "gap_persen_sep2025",
            "rankApr2025vsSep2025": "rank_sep2025",
            "harga_2026-04-01": "harga_1_apr_2026",
            "gap_idr_rankApr2025vsApr2026": "gap_rp_apr2026",
            "gap_persen_rankApr2025vsApr2026": "gap_persen_apr2026",
            "rankApr2025vsApr2026": "rank_apr2026",
        }
    )
    display_cols = [
        "kode",
        "nama",
        "harga_8_apr_2025",
        "harga_1_sep_2025",
        "gap_rp_sep2025",
        "gap_persen_sep2025",
        "rank_sep2025",
        "harga_1_apr_2026",
        "gap_rp_apr2026",
        "gap_persen_apr2026",
        "rank_apr2026",
    ]
    print(combined[display_cols].to_string(index=False))
