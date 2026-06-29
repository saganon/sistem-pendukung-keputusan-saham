from dataclasses import dataclass
from datetime import datetime


@dataclass
class StockInfo:
    stock_code: str
    fiscal_year: int
    fiscal_period_end: datetime | None
    audit_publication_date: datetime | None
    stock_price_date: datetime | None
    financial_currency: str | None
    market_currency: str | None
    usd_to_idr_rate: float | None
    fx_rate_date: datetime | None
    market_cap: float | None
    per: float | None
    price_to_book: float | None
    return_on_assets: float | None
    debt_to_equity: float | None
    stock_price: float | None
    eps: float | None
    bvps: float | None
    eps_report_currency: float | None
    bvps_report_currency: float | None
    graham_number: float
    valuation_status: str
    currency: str
    total_assets: float | None = None
    total_liabilities: float | None = None
    total_equity: float | None = None
    parent_equity: float | None = None
    total_profit: float | None = None
    parent_net_income: float | None = None
    earnings_per_share: float | None = None
    shares_outstanding: float | None = None
    unit_divisor: float | None = None

    @property
    def current_price(self) -> float | None:
        """Alias kompatibilitas — harga pada tanggal publikasi 2025."""
        return self.stock_price

    @property
    def report_date(self) -> datetime | None:
        """Alias kompatibilitas — tanggal publikasi audit."""
        return self.audit_publication_date
