from dataclasses import dataclass

import numpy as np
import pandas as pd

from dss_stock.calculation_log import (
    configure_calculation_logging,
    fmt,
    log_dataframe,
    log_section,
    log_series,
    log_step,
    log_text,
)
from dss_stock.entity.stock_info import StockInfo

CRITERIA_COLUMNS = ("ROA", "DER", "PBV", "EPS")


@dataclass
class EntropySteps:
    """Hasil per langkah perhitungan Entropy sesuai skripsi."""

    decision_matrix: pd.DataFrame
    column_totals: pd.Series
    proportion_matrix: pd.DataFrame
    ln_proportion_matrix: pd.DataFrame
    p_times_ln_p_matrix: pd.DataFrame
    sum_p_ln_p: pd.Series
    n_alternatives: int
    k_constant: float
    entropy: pd.Series
    diversification: pd.Series
    weights: pd.Series


def build_decision_matrix(stocks: list[StockInfo]) -> pd.DataFrame:
    """Bangun matriks keputusan dari saham undervalued (data yfinance)."""
    rows = []
    for stock in stocks:
        rows.append(
            {
                "ROA": stock.return_on_assets * 100,
                "DER": stock.debt_to_equity,
                "PBV": stock.price_to_book,
                "EPS": stock.eps,
            }
        )
    return pd.DataFrame(rows, index=[stock.stock_code for stock in stocks])


def calculate_entropy_steps(df_input: pd.DataFrame) -> EntropySteps:
    """Hitung bobot Entropy dengan output setiap langkah perhitungan.

    Rumus (skripsi v1 - rumus.pdf):
      p_ij = x_ij / Σ x_ij
      k    = 1 / ln(n)
      E_j  = -k × Σ (p_ij × ln(p_ij))
      d_j  = 1 - E_j
      w_j  = d_j / Σ d_j
    """
    configure_calculation_logging()

    df = df_input.copy()
    n = len(df)
    if n < 2:
        raise ValueError("Entropy membutuhkan minimal 2 alternatif saham undervalued.")

    log_section("METODE ENTROPY — Log Perhitungan Lengkap")
    log_text(f"Jumlah alternatif (n) = {n}")
    log_text(f"Kriteria = {list(df.columns)}")

    log_step(
        1,
        "Matriks Keputusan Awal (x_ij)",
        "x_ij dari data yfinance: ROA (%), DER, PBV, EPS (hanya saham undervalued)",
    )
    log_dataframe("Matriks keputusan D", df)

    column_totals = df.sum(axis=0)
    log_step(2, "Total per Kriteria", "Σ_i x_ij  (jumlah kolom)")
    for col in df.columns:
        parts = " + ".join(fmt(df.loc[idx, col]) for idx in df.index)
        log_text(f"  Σ {col} = {parts} = {fmt(column_totals[col])}")
    log_series("Hasil Σ x_ij", column_totals)

    proportion_matrix = df.div(column_totals, axis=1)
    log_step(3, "Normalisasi Proporsi", "p_ij = x_ij / Σ_i x_ij")
    for idx in df.index:
        for col in df.columns:
            x_ij = float(df.loc[idx, col])
            total = float(column_totals[col])
            p_ij = float(proportion_matrix.loc[idx, col])
            log_text(
                f"  p[{idx},{col}] = {fmt(x_ij)} / {fmt(total)} = {fmt(p_ij)}"
            )
    log_dataframe("Matriks proporsi p_ij", proportion_matrix)

    ln_proportion_matrix = proportion_matrix.map(
        lambda value: np.log(value) if value > 0 else 0.0
    )
    log_step(4, "Logaritma Natural Proporsi", "ln(p_ij); jika p_ij = 0 maka 0")
    for idx in proportion_matrix.index:
        for col in proportion_matrix.columns:
            p_ij = float(proportion_matrix.loc[idx, col])
            ln_p = float(ln_proportion_matrix.loc[idx, col])
            if p_ij > 0:
                log_text(f"  ln(p[{idx},{col}]) = ln({fmt(p_ij)}) = {fmt(ln_p)}")
            else:
                log_text(f"  ln(p[{idx},{col}]) = 0  (karena p_ij = 0)")
    log_dataframe("Matriks ln(p_ij)", ln_proportion_matrix)

    p_times_ln_p_matrix = proportion_matrix * ln_proportion_matrix
    log_step(5, "Perkalian p_ij × ln(p_ij)", "p_ij × ln(p_ij)")
    for idx in proportion_matrix.index:
        for col in proportion_matrix.columns:
            p_ij = float(proportion_matrix.loc[idx, col])
            ln_p = float(ln_proportion_matrix.loc[idx, col])
            product = float(p_times_ln_p_matrix.loc[idx, col])
            log_text(
                f"  p×ln(p)[{idx},{col}] = {fmt(p_ij)} × {fmt(ln_p)} = {fmt(product)}"
            )
    log_dataframe("Matriks p_ij × ln(p_ij)", p_times_ln_p_matrix)

    sum_p_ln_p = p_times_ln_p_matrix.sum(axis=0)
    log_step(6, "Jumlah p_ij × ln(p_ij) per Kriteria", "Σ_i (p_ij × ln(p_ij))")
    for col in p_times_ln_p_matrix.columns:
        parts = " + ".join(
            fmt(p_times_ln_p_matrix.loc[idx, col]) for idx in p_times_ln_p_matrix.index
        )
        log_text(f"  Σ {col} = {parts} = {fmt(sum_p_ln_p[col])}")
    log_series("Hasil Σ (p_ij × ln(p_ij))", sum_p_ln_p)

    k_constant = 1.0 / np.log(n)
    log_step(7, "Konstanta Entropy", "k = 1 / ln(n)")
    log_text(f"  ln(n) = ln({n}) = {fmt(np.log(n))}")
    log_text(f"  k = 1 / {fmt(np.log(n))} = {fmt(k_constant)}")

    entropy = -k_constant * sum_p_ln_p
    log_step(8, "Nilai Entropy per Kriteria", "E_j = -k × Σ_i (p_ij × ln(p_ij))")
    for col in entropy.index:
        log_text(
            f"  E[{col}] = -({fmt(k_constant)}) × ({fmt(sum_p_ln_p[col])}) "
            f"= {fmt(entropy[col])}"
        )
    log_series("Hasil E_j", entropy)

    diversification = 1.0 - entropy
    log_step(9, "Tingkat Diversifikasi", "d_j = 1 - E_j")
    for col in diversification.index:
        log_text(
            f"  d[{col}] = 1 - {fmt(entropy[col])} = {fmt(diversification[col])}"
        )
    log_series("Hasil d_j", diversification)

    sum_d = float(diversification.sum())
    weights = diversification / diversification.sum()
    log_step(10, "Bobot Entropy Final", "w_j = d_j / Σ_j d_j")
    parts = " + ".join(fmt(diversification[col]) for col in diversification.index)
    log_text(f"  Σ d_j = {parts} = {fmt(sum_d)}")
    for col in weights.index:
        log_text(
            f"  w[{col}] = {fmt(diversification[col])} / {fmt(sum_d)} "
            f"= {fmt(weights[col])} ({fmt(weights[col] * 100)}%)"
        )
    log_series("Hasil w_j", weights)
    log_text("Entropy selesai.")

    return EntropySteps(
        decision_matrix=df,
        column_totals=column_totals,
        proportion_matrix=proportion_matrix,
        ln_proportion_matrix=ln_proportion_matrix,
        p_times_ln_p_matrix=p_times_ln_p_matrix,
        sum_p_ln_p=sum_p_ln_p,
        n_alternatives=n,
        k_constant=k_constant,
        entropy=entropy,
        diversification=diversification,
        weights=weights,
    )


def calculate_entropy_weights(df_input: pd.DataFrame) -> pd.Series:
    """Hitung bobot kriteria — kompatibilitas dengan modul TOPSIS."""
    return calculate_entropy_steps(df_input).weights
