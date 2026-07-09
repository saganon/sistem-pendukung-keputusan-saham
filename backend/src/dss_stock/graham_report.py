"""Cetak tabel hasil screening Benjamin Graham."""

import pandas as pd

from dss_stock.constants import STOCK_NAMES
from dss_stock.entity.stock_info import StockInfo
from dss_stock.under_value_stock import screen_graham_undervalued

GRAHAM_FORMULAS = {
    "graham_number": "GN = √(22,5 × EPS × BVPS)",
    "kriteria": "Undervalued jika Harga Saham < Graham Number",
    "eps": "EPS (IDR) dari laporan keuangan tahunan",
    "bvps": "BVPS (IDR) = Ekuitas Induk / Saham Beredar (dikonversi ke IDR jika USD)",
}


def _format_status(status: str) -> str:
    mapping = {
        "undervalued": "Undervalued",
        "overvalued": "Overvalued",
        "tidak_valid": "Tidak Valid",
    }
    return mapping.get(status, status)


def build_graham_table(stocks: list[StockInfo]) -> pd.DataFrame:
    """Bangun tabel ringkas hasil perhitungan Graham."""
    rows: list[dict[str, object]] = []
    for stock in stocks:
        harga = stock.stock_price or 0.0
        graham = stock.graham_number
        margin_idr = graham - harga if graham > 0 else None
        margin_pct = ((graham / harga) - 1) * 100 if harga > 0 and graham > 0 else None

        rows.append(
            {
                "kode": stock.stock_code,
                "nama": STOCK_NAMES.get(stock.stock_code, stock.stock_code),
                "eps_idr": stock.eps,
                "bvps_idr": stock.bvps,
                "roa_pct": (stock.return_on_assets or 0) * 100,
                "der": stock.debt_to_equity,
                "pbv": stock.price_to_book,
                "harga_saham": harga,
                "graham_number": graham,
                "margin_idr": margin_idr,
                "margin_pct": margin_pct,
                "klasifikasi": _format_status(stock.valuation_status),
            }
        )

    return pd.DataFrame(rows)


def print_graham_tables(stocks: list[StockInfo]) -> None:
    """Cetak tabel Graham ke terminal dengan format rapi."""
    if not stocks:
        print("\nTidak ada data saham untuk ditampilkan.")
        return

    pd.options.display.float_format = "{:,.2f}".format
    pd.options.display.max_columns = None
    pd.options.display.width = None

    df = build_graham_table(stocks)

    print("\n=== METODE GRAHAM — Rumus ===")
    for key, formula in GRAHAM_FORMULAS.items():
        print(f"  {key}: {formula}")

    print("\n--- Tabel Hasil Screening Graham (Semua Emiten) ---")
    display_all = df[
        [
            "kode",
            "nama",
            "eps_idr",
            "bvps_idr",
            "roa_pct",
            "der",
            "pbv",
            "harga_saham",
            "graham_number",
            "margin_idr",
            "margin_pct",
            "klasifikasi",
        ]
    ].rename(
        columns={
            "eps_idr": "eps",
            "bvps_idr": "bvps",
            "roa_pct": "roa_%",
            "harga_saham": "harga",
            "graham_number": "graham_num",
            "margin_idr": "selisih_rp",
            "margin_pct": "selisih_%",
        }
    )
    print(display_all.to_string(index=False))

    undervalued = df[df["klasifikasi"] == "Undervalued"]
    total = len(df)
    lolos = len(undervalued)

    print("\n--- Ringkasan Screening ---")
    print(f"  Total emiten dianalisis : {total}")
    print(f"  Lolos (Undervalued)     : {lolos}")
    print(f"  Tidak lolos             : {total - lolos}")

    if not undervalued.empty:
        print("\n--- Saham Undervalued (Lolos Pre-filtering) ---")
        display_uv = undervalued[
            [
                "kode",
                "nama",
                "harga_saham",
                "graham_number",
                "margin_pct",
                "klasifikasi",
            ]
        ].rename(
            columns={
                "harga_saham": "harga",
                "graham_number": "graham_num",
                "margin_pct": "selisih_%",
            }
        )
        print(display_uv.to_string(index=False))


def run_graham_analysis(
    verbose: bool = False,
    sleep_seconds: float = 1.0,
) -> tuple[list[StockInfo], list[StockInfo]]:
    """Jalankan screening Graham lalu cetak tabel hasil ke terminal."""
    print("Mengambil data dan menghitung screening Graham...")
    undervalued_stocks, all_results = screen_graham_undervalued(
        verbose=verbose,
        sleep_seconds=sleep_seconds,
    )

    if all_results:
        print_graham_tables(all_results)

    return undervalued_stocks, all_results
