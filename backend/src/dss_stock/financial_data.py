from dataclasses import dataclass
from datetime import datetime

from dss_stock.audit_input import AuditInputData, FISCAL_YEAR, fetch_audit_input


@dataclass
class AnnualFinancials:
    stock_code: str
    fiscal_year: int
    audit_publication_date: datetime | None
    stock_price_date: datetime | None
    financial_currency: str | None
    market_currency: str | None
    usd_to_idr_rate: float | None
    fx_rate_date: datetime | None
    eps: float | None
    bvps: float | None
    eps_report_currency: float | None
    bvps_report_currency: float | None
    net_income: float | None
    stockholders_equity: float | None
    shares_outstanding: float | None
    stock_price: float | None
    market_cap: float | None
    per: float | None
    price_to_book: float | None
    return_on_assets: float | None
    debt_to_equity: float | None
    total_assets: float | None
    total_liabilities: float | None
    total_equity: float | None
    total_profit: float | None


def _audit_input_to_annual_financials(audit: AuditInputData) -> AnnualFinancials:
    """Turunkan metrik valuasi dari data input audit (rumus Simulasi.xlsx)."""
    eps_report_currency = audit.earnings_per_share
    bvps_report_currency = audit.parent_equity / audit.shares_outstanding

    eps = eps_report_currency
    bvps = bvps_report_currency
    if audit.financial_currency == "USD" and audit.market_currency == "IDR":
        eps = eps_report_currency * audit.conversion_rate
        bvps = bvps_report_currency * audit.conversion_rate

    stock_price = audit.stock_price
    price_to_book = stock_price / bvps if stock_price is not None and bvps > 0 else None
    per = stock_price / eps if stock_price is not None and eps > 0 else None
    market_cap = (
        stock_price * audit.shares_outstanding if stock_price is not None else None
    )

    return_on_assets = audit.total_profit / audit.total_assets
    debt_to_equity = audit.total_liabilities / audit.total_equity

    return AnnualFinancials(
        stock_code=audit.stock_code,
        fiscal_year=audit.fiscal_year,
        audit_publication_date=audit.audit_publication_date,
        stock_price_date=audit.stock_price_date,
        financial_currency=audit.financial_currency,
        market_currency=audit.market_currency,
        usd_to_idr_rate=audit.conversion_rate if audit.financial_currency == "USD" else None,
        fx_rate_date=audit.conversion_rate_date,
        eps=eps,
        bvps=bvps,
        eps_report_currency=eps_report_currency,
        bvps_report_currency=bvps_report_currency,
        net_income=audit.parent_net_income,
        stockholders_equity=audit.parent_equity,
        shares_outstanding=audit.shares_outstanding,
        stock_price=stock_price,
        market_cap=market_cap,
        per=per,
        price_to_book=price_to_book,
        return_on_assets=return_on_assets,
        debt_to_equity=debt_to_equity,
        total_assets=audit.total_assets,
        total_liabilities=audit.total_liabilities,
        total_equity=audit.total_equity,
        total_profit=audit.total_profit,
    )


def fetch_annual_financials(
    stock_code: str,
    fiscal_year: int = FISCAL_YEAR,
) -> AnnualFinancials:
    """Ambil data laporan keuangan tahunan dan metrik turunannya."""
    audit = fetch_audit_input(stock_code=stock_code, fiscal_year=fiscal_year)
    return _audit_input_to_annual_financials(audit)
