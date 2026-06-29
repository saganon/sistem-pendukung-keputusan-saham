"""Ambil data input laporan audit tahun fiskal dari Yahoo Finance.

Laporan keuangan: tahun fiskal 2024 (kolom 2024-12-31).
Konteks publikasi: tahun 2025 — kurs dan harga saham diambil historis
pada tanggal publikasi, bukan data terkini.
"""

import tempfile
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import yfinance as yf

try:
    yf.set_tz_cache_location(tempfile.gettempdir())
except Exception:
    pass

FISCAL_YEAR = 2024
PUBLICATION_YEAR = 2025

# Tanggal laporan audit FY2024 (publikasi 2025) — Simulasi.xlsx baris 4
AUDIT_PUBLICATION_DATES: dict[str, str] = {
    "ADMR": "2025-02-27",
    "ADRO": "2025-02-28",
    "AKRA": "2025-03-18",
    "ITMG": "2025-02-26",
    "MEDC": "2025-03-28",
    "PGAS": "2025-03-21",
    "PTBA": "2025-03-26",
}

# Tanggal acuan harga saham — Simulasi.xlsx Sheet2 (8 Apr 2025)
STOCK_VALUATION_DATE = "2025-04-08"

_fx_rate_cache: dict[str, tuple[float, datetime]] = {}
_price_cache: dict[str, tuple[float, datetime]] = {}

ASSET_ROW = "Total Assets"
LIABILITY_ROW = "Total Liabilities Net Minority Interest"
TOTAL_EQUITY_ROWS = (
    "Total Equity Gross Minority Interest",
    "Total Stockholder Equity",
    "Stockholders Equity",
)
PARENT_EQUITY_ROWS = (
    "Stockholders Equity",
    "Common Stock Equity",
)
PARENT_NET_INCOME_ROWS = (
    "Net Income Common Stockholders",
    "Net Income",
)
TOTAL_PROFIT_ROWS = (
    "Net Income Including Noncontrolling Interests",
    "Net Income Continuous Operations",
    "Pretax Income",
)
EPS_ROWS = (
    "Basic EPS",
    "Diluted EPS",
)
SHARES_ROWS = (
    "Ordinary Shares Number",
    "Basic Average Shares",
)


@dataclass
class AuditInputData:
    """Data input laporan audit — mirror baris 3-13 Simulasi.xlsx."""

    stock_code: str
    fiscal_year: int
    fiscal_period_end: datetime
    audit_publication_date: datetime
    stock_price_date: datetime
    financial_currency: str | None
    market_currency: str | None
    unit_divisor: float
    conversion_rate: float
    conversion_rate_date: datetime | None
    total_assets: float
    total_liabilities: float
    total_equity: float
    parent_equity: float
    total_profit: float
    parent_net_income: float
    earnings_per_share: float
    shares_outstanding: float
    stock_price: float | None


def _find_fiscal_column(columns: pd.Index, year: int) -> pd.Timestamp | None:
    for column in columns:
        if hasattr(column, "year") and column.year == year:
            return column
    return None


def _first_available_row(df: pd.DataFrame, row_names: tuple[str, ...]) -> str | None:
    for row_name in row_names:
        if row_name in df.index:
            return row_name
    return None


def _get_row_value(df: pd.DataFrame, row_names: tuple[str, ...], column) -> float:
    row_name = _first_available_row(df, row_names)
    if row_name is None:
        available = ", ".join(df.index[:10])
        raise ValueError(f"Baris tidak ditemukan ({row_names}). Contoh: {available}")
    value = df.loc[row_name, column]
    if pd.isna(value):
        raise ValueError(f"Nilai kosong untuk baris {row_name}.")
    return float(value)


def _normalize_timestamp(value: pd.Timestamp) -> pd.Timestamp:
    if value.tzinfo is not None:
        return value.tz_convert(None)
    return value


def get_historical_close_at_date(
    symbol: str,
    target_date: pd.Timestamp,
) -> tuple[float, datetime]:
    """Ambil harga penutupan historis (Close, bukan Adj Close) pada tanggal target."""
    target_date = _normalize_timestamp(target_date)
    cache_key = f"{symbol}:{target_date.strftime('%Y-%m-%d')}"
    if cache_key in _price_cache:
        return _price_cache[cache_key]

    ticker = yf.Ticker(symbol)
    start_date = target_date - pd.Timedelta(days=21)
    end_date = target_date + pd.Timedelta(days=1)
    history = ticker.history(start=start_date, end=end_date, auto_adjust=False)

    if history.empty:
        raise ValueError(
            f"Tidak dapat mengambil harga historis {symbol} "
            f"untuk tanggal {target_date.strftime('%Y-%m-%d')}."
        )

    history.index = history.index.tz_localize(None)
    eligible = history[history.index <= target_date]

    if eligible.empty:
        price = float(history["Close"].iloc[0])
        actual_date = history.index[0].to_pydatetime()
    else:
        price = float(eligible["Close"].iloc[-1])
        actual_date = eligible.index[-1].to_pydatetime()

    result = (price, actual_date)
    _price_cache[cache_key] = result
    return result


def get_usd_to_idr_rate_at_date(report_date: pd.Timestamp) -> tuple[float, datetime]:
    """Ambil kurs USD/IDR historis pada atau sebelum tanggal target."""
    return get_historical_close_at_date("USDIDR=X", report_date)


def _infer_unit_divisor(value: float) -> float:
    """Tentukan pembagi satuan tampilan seperti di Simulasi.xlsx."""
    abs_value = abs(value)
    if abs_value >= 1e15:
        return 1_000_000.0
    if abs_value >= 1e10:
        return 1_000.0
    return 1.0


def _resolve_audit_publication_date(stock_code: str) -> pd.Timestamp:
    date_str = AUDIT_PUBLICATION_DATES.get(stock_code)
    if date_str is None:
        raise ValueError(
            f"Tanggal publikasi audit {stock_code} belum dikonfigurasi "
            f"untuk tahun {PUBLICATION_YEAR}."
        )
    return pd.Timestamp(date_str)


def fetch_audit_input(
    stock_code: str,
    fiscal_year: int = FISCAL_YEAR,
) -> AuditInputData:
    """Ambil data input laporan audit tahun fiskal dari Yahoo Finance."""
    ticker = yf.Ticker(f"{stock_code}.JK")
    info = ticker.info

    financials = ticker.financials
    balance_sheet = ticker.balance_sheet

    if financials is None or financials.empty:
        raise ValueError(f"Laporan laba rugi {stock_code} tidak tersedia.")
    if balance_sheet is None or balance_sheet.empty:
        raise ValueError(f"Laporan neraca {stock_code} tidak tersedia.")

    fiscal_column = _find_fiscal_column(financials.columns, fiscal_year)
    if fiscal_column is None:
        available_years = sorted(
            {column.year for column in financials.columns if hasattr(column, "year")}
        )
        raise ValueError(
            f"Laporan audit tahun fiskal {fiscal_year} untuk {stock_code} "
            f"tidak ditemukan. Tahun tersedia: {available_years}"
        )

    if fiscal_column not in balance_sheet.columns:
        raise ValueError(
            f"Neraca tahun fiskal {fiscal_year} untuk {stock_code} tidak ditemukan."
        )

    fiscal_period_end = _normalize_timestamp(fiscal_column)
    audit_publication_date = _resolve_audit_publication_date(stock_code)
    stock_price_date = pd.Timestamp(STOCK_VALUATION_DATE)

    financial_currency = info.get("financialCurrency")
    market_currency = info.get("currency")

    total_assets = _get_row_value(balance_sheet, (ASSET_ROW,), fiscal_column)
    total_liabilities = _get_row_value(balance_sheet, (LIABILITY_ROW,), fiscal_column)
    parent_equity = _get_row_value(balance_sheet, PARENT_EQUITY_ROWS, fiscal_column)

    try:
        total_equity = _get_row_value(balance_sheet, TOTAL_EQUITY_ROWS, fiscal_column)
    except ValueError:
        total_equity = parent_equity

    parent_net_income = _get_row_value(financials, PARENT_NET_INCOME_ROWS, fiscal_column)

    try:
        total_profit = _get_row_value(financials, TOTAL_PROFIT_ROWS, fiscal_column)
    except ValueError:
        total_profit = parent_net_income

    try:
        earnings_per_share = _get_row_value(financials, EPS_ROWS, fiscal_column)
    except ValueError:
        shares_row = _first_available_row(balance_sheet, SHARES_ROWS)
        if shares_row is None:
            raise ValueError(f"EPS dan jumlah saham {stock_code} tidak tersedia.")
        shares_count = float(balance_sheet.loc[shares_row, fiscal_column])
        earnings_per_share = parent_net_income / shares_count

    if earnings_per_share == 0:
        raise ValueError(f"Laba per saham {stock_code} bernilai nol.")

    shares_outstanding = parent_net_income / earnings_per_share

    conversion_rate = 1.0
    conversion_rate_date = None
    if financial_currency == "USD" and market_currency == "IDR":
        conversion_rate, conversion_rate_date = get_usd_to_idr_rate_at_date(
            audit_publication_date
        )

    stock_price, _ = get_historical_close_at_date(
        f"{stock_code}.JK",
        stock_price_date,
    )

    unit_divisor = _infer_unit_divisor(total_assets)

    return AuditInputData(
        stock_code=stock_code,
        fiscal_year=fiscal_year,
        fiscal_period_end=fiscal_period_end.to_pydatetime(),
        audit_publication_date=audit_publication_date.to_pydatetime(),
        stock_price_date=stock_price_date.to_pydatetime(),
        financial_currency=financial_currency,
        market_currency=market_currency,
        unit_divisor=unit_divisor,
        conversion_rate=conversion_rate,
        conversion_rate_date=conversion_rate_date,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        total_equity=total_equity,
        parent_equity=parent_equity,
        total_profit=total_profit,
        parent_net_income=parent_net_income,
        earnings_per_share=earnings_per_share,
        shares_outstanding=shares_outstanding,
        stock_price=stock_price,
    )
