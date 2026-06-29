from dataclasses import dataclass

import numpy as np
import pandas as pd

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
    df = df_input.copy()
    n = len(df)
    if n < 2:
        raise ValueError("Entropy membutuhkan minimal 2 alternatif saham undervalued.")

    column_totals = df.sum(axis=0)
    proportion_matrix = df.div(column_totals, axis=1)

    ln_proportion_matrix = proportion_matrix.map(
        lambda value: np.log(value) if value > 0 else 0.0
    )
    p_times_ln_p_matrix = proportion_matrix * ln_proportion_matrix
    sum_p_ln_p = p_times_ln_p_matrix.sum(axis=0)

    k_constant = 1.0 / np.log(n)
    entropy = -k_constant * sum_p_ln_p
    diversification = 1.0 - entropy
    weights = diversification / diversification.sum()

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
