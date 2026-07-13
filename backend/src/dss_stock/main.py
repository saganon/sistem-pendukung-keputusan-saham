from dss_stock.backtesting_report import print_backtesting_tables, run_backtesting_analysis
from dss_stock.calculation_log import configure_calculation_logging
from dss_stock.entropy_report import print_entropy_tables, run_entropy_analysis
from dss_stock.graham_report import run_graham_analysis
from dss_stock.topsis_report import print_topsis_tables, run_topsis_analysis


def main() -> None:
    configure_calculation_logging()
    undervalued_stocks, all_results = run_graham_analysis(verbose=False)

    if not all_results:
        print("\nTidak ada data saham yang berhasil diproses.")
        return

    if not undervalued_stocks:
        print("\nTidak ada saham yang memenuhi kriteria undervalued.")
        return

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
