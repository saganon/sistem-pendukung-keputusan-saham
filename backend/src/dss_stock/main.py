import pandas as pd

from dss_stock.backtesting_report import print_backtesting_tables, run_backtesting_analysis
from dss_stock.entropy_report import print_entropy_tables, run_entropy_analysis
from dss_stock.report import build_merged_screening_table, print_formula_legend
from dss_stock.topsis_report import print_topsis_tables, run_topsis_analysis
from dss_stock.under_value_stock import screen_graham_undervalued


def main() -> None:
    undervalued_stocks, all_results = screen_graham_undervalued()

    if not all_results:
        print("\nTidak ada data saham yang berhasil diproses.")
        return

    df_merged = build_merged_screening_table(all_results)

    pd.options.display.float_format = "{:,.4f}".format
    pd.options.display.max_columns = None
    pd.options.display.width = None

    print("\n=== Tabel Gabungan: Data yfinance + Perhitungan + Screening ===")
    print_formula_legend()
    print(df_merged.to_string(index=False))

    print("\n=== Saham Undervalued (lolos pre-filtering) ===")
    df_undervalued = df_merged[df_merged["status"] == "undervalued"]
    if df_undervalued.empty:
        print("Tidak ada saham yang memenuhi kriteria undervalued.")
        return

    print(df_undervalued.to_string(index=False))

    if len(undervalued_stocks) < 2:
        print(
            "\nEntropy/TOPSIS tidak dihitung: minimal 2 saham undervalued "
            f"(saat ini {len(undervalued_stocks)})."
        )
        return

    _, entropy_steps = run_entropy_analysis(undervalued_stocks)
    print_entropy_tables(entropy_steps)

    topsis_steps = run_topsis_analysis(undervalued_stocks, entropy_steps)
    print_topsis_tables(topsis_steps)

    stock_codes = [stock.stock_code for stock in undervalued_stocks]
    backtesting_steps = run_backtesting_analysis(stock_codes)
    print_backtesting_tables(backtesting_steps)


if __name__ == "__main__":
    main()
