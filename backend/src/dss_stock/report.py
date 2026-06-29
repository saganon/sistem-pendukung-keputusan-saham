import pandas as pd

from dss_stock.entity.stock_info import StockInfo

FORMULA_LEGEND = {
    "roa": "Jumlah Laba / Jumlah Aset",
    "der": "Jumlah Liabilitas / Jumlah Ekuitas",
    "eps_idr": "LPS × Kurs Konversi (IDR jika laporan USD)",
    "bvps_idr": "(Ekuitas Induk / Saham Beredar) × Kurs Konversi",
    "pbv": "Harga Saham / BVPS (IDR)",
    "per": "Harga Saham / EPS (IDR)",
    "graham_number": "√(22,5 × EPS × BVPS)",
    "valuation_status": "Undervalued jika Harga Saham < Graham Number",
}


def build_merged_screening_table(stocks: list[StockInfo]) -> pd.DataFrame:
    """Gabungkan data mentah yfinance dengan metrik turunan dan hasil screening."""
    rows = []
    for stock in stocks:
        rows.append(
            {
                "saham": stock.stock_code,
                "tahun_fiskal": stock.fiscal_year,
                "tanggal_publikasi_audit": stock.audit_publication_date,
                "tanggal_harga_saham": stock.stock_price_date,
                "mata_uang_laporan": stock.financial_currency,
                "kurs_usd_idr": stock.usd_to_idr_rate,
                "jumlah_aset": stock.total_assets,
                "jumlah_liabilitas": stock.total_liabilities,
                "jumlah_ekuitas": stock.total_equity,
                "ekuitas_induk": stock.parent_equity,
                "jumlah_laba": stock.total_profit,
                "laba_induk": stock.parent_net_income,
                "laba_per_saham": stock.earnings_per_share,
                "saham_beredar": stock.shares_outstanding,
                "harga_saham": stock.stock_price,
                "roa": stock.return_on_assets,
                "der": stock.debt_to_equity,
                "eps_idr": stock.eps,
                "bvps_idr": stock.bvps,
                "pbv": stock.price_to_book,
                "per": stock.per,
                "graham_number": stock.graham_number,
                "status": stock.valuation_status,
            }
        )
    return pd.DataFrame(rows)


def print_formula_legend() -> None:
    print("=== Rumus Perhitungan ===")
    for field, formula in FORMULA_LEGEND.items():
        print(f"  {field}: {formula}")
    print()
