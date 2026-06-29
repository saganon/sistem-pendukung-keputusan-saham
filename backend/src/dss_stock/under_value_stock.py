import time
from pathlib import Path

from dss_stock.audit_input import FISCAL_YEAR, PUBLICATION_YEAR, fetch_audit_input
from dss_stock.entity.stock_info import StockInfo
from dss_stock.financial_data import fetch_annual_financials
from dss_stock.graham_formula import GrahamFormula

BASE_DIR = Path(__file__).resolve().parent
STOCK_LIST_PATH = BASE_DIR.parent.parent / "list_stock_code.txt"


def _load_stock_codes() -> list[str]:
    with open(STOCK_LIST_PATH, encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def screen_graham_undervalued(
    fiscal_year: int = FISCAL_YEAR,
    sleep_seconds: float = 1.0,
) -> tuple[list[StockInfo], list[StockInfo]]:
    """Hitung Graham Number dan kategorikan saham undervalued/overvalued."""
    print(
        f"Mengambil data input laporan audit tahun fiskal {fiscal_year} "
        f"(publikasi {PUBLICATION_YEAR}) dari Yahoo Finance..."
    )
    print("Rumus: Graham Number = sqrt(22.5 x EPS x BVPS)")
    print("Kriteria undervalued: harga pasar < Graham Number")
    print(
        "Semua data pasar & kurs: historis tahun publikasi 2025 "
        "(bukan data terkini)\n"
    )

    all_results: list[StockInfo] = []
    undervalued_stocks: list[StockInfo] = []

    for stock_code in _load_stock_codes():
        print(f"Memproses {stock_code}...")
        try:
            audit = fetch_audit_input(stock_code=stock_code, fiscal_year=fiscal_year)
            financials = fetch_annual_financials(
                stock_code=stock_code,
                fiscal_year=fiscal_year,
            )
        except ValueError as error:
            print(f"  Gagal: {error}")
            print("-" * 40)
            time.sleep(sleep_seconds)
            continue

        _print_audit_input(audit)

        if GrahamFormula.is_applicable(financials.eps, financials.bvps):
            graham_number = GrahamFormula.calculate(
                eps=financials.eps,
                bvps=financials.bvps,
            )
        else:
            print(
                f"  Graham Number tidak berlaku: EPS={financials.eps}, "
                f"BVPS={financials.bvps}"
            )
            graham_number = 0.0

        valuation_status = GrahamFormula.classify(
            current_price=financials.stock_price,
            graham_number=graham_number,
        )

        stock_info = StockInfo(
            stock_code=stock_code,
            fiscal_year=fiscal_year,
            fiscal_period_end=audit.fiscal_period_end,
            audit_publication_date=audit.audit_publication_date,
            stock_price_date=audit.stock_price_date,
            financial_currency=audit.financial_currency,
            market_currency=audit.market_currency,
            usd_to_idr_rate=audit.conversion_rate
            if audit.financial_currency == "USD"
            else None,
            fx_rate_date=audit.conversion_rate_date,
            market_cap=financials.market_cap,
            per=financials.per,
            price_to_book=financials.price_to_book,
            return_on_assets=financials.return_on_assets,
            debt_to_equity=financials.debt_to_equity,
            stock_price=financials.stock_price,
            eps=financials.eps,
            bvps=financials.bvps,
            eps_report_currency=financials.eps_report_currency,
            bvps_report_currency=financials.bvps_report_currency,
            graham_number=graham_number,
            valuation_status=valuation_status,
            currency=audit.market_currency or "IDR",
            total_assets=audit.total_assets,
            total_liabilities=audit.total_liabilities,
            total_equity=audit.total_equity,
            parent_equity=audit.parent_equity,
            total_profit=audit.total_profit,
            parent_net_income=audit.parent_net_income,
            earnings_per_share=audit.earnings_per_share,
            shares_outstanding=audit.shares_outstanding,
            unit_divisor=audit.unit_divisor,
        )
        all_results.append(stock_info)

        print(f"  ROA: {financials.return_on_assets:.4%}")
        print(f"  DER: {financials.debt_to_equity:.4f}")
        print(f"  EPS (IDR): {financials.eps:,.4f}")
        print(f"  BVPS (IDR): {financials.bvps:,.4f}")
        print(f"  PBV: {financials.price_to_book:,.4f}")
        print(
            f"  Harga saham ({audit.stock_price_date:%Y-%m-%d}): "
            f"{financials.stock_price:,.2f}"
        )
        print(f"  Graham Number: {graham_number:,.2f}")
        print(f"  Status: {valuation_status}")

        if valuation_status == "undervalued":
            undervalued_stocks.append(stock_info)

        print("-" * 40)
        time.sleep(sleep_seconds)

    return undervalued_stocks, all_results


def _print_audit_input(audit) -> None:
    print(f"  Periode fiskal berakhir: {audit.fiscal_period_end:%Y-%m-%d}")
    print(f"  Tanggal publikasi audit: {audit.audit_publication_date:%Y-%m-%d}")
    print(f"  Mata uang laporan: {audit.financial_currency}")
    if audit.financial_currency == "USD":
        print(
            f"  Kurs USD/IDR ({audit.conversion_rate_date:%Y-%m-%d}): "
            f"{audit.conversion_rate:,.2f}"
        )
    print(f"  Satuan (pembagi tampilan): {audit.unit_divisor:,.0f}")
    print(f"  Jumlah Aset: {audit.total_assets:,.0f}")
    print(f"  Jumlah Liabilitas: {audit.total_liabilities:,.0f}")
    print(f"  Jumlah Ekuitas: {audit.total_equity:,.0f}")
    print(f"  Ekuitas Induk: {audit.parent_equity:,.0f}")
    print(f"  Jumlah Laba: {audit.total_profit:,.0f}")
    print(f"  Laba Induk: {audit.parent_net_income:,.0f}")
    print(
        f"  Laba per Saham ({audit.financial_currency}): "
        f"{audit.earnings_per_share:,.6f}"
    )
    print(f"  Jumlah Saham Beredar: {audit.shares_outstanding:,.0f}")


def under_value_stock() -> list[StockInfo]:
    """Kompatibilitas dengan modul lain: kembalikan saham undervalued saja."""
    undervalued_stocks, _ = screen_graham_undervalued()
    return undervalued_stocks
