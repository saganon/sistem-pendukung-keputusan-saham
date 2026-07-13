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

CRITERIA_TYPES = {
    "ROA": "benefit",
    "DER": "cost",
    "PBV": "cost",
    "EPS": "benefit",
}


@dataclass
class TopsisSteps:
    """Hasil per langkah perhitungan TOPSIS sesuai skripsi."""

    decision_matrix: pd.DataFrame
    entropy_weights: pd.Series
    criteria_types: dict[str, str]
    norm_factor: pd.Series
    normalized_matrix: pd.DataFrame
    weighted_matrix: pd.DataFrame
    ideal_positive: pd.Series
    ideal_negative: pd.Series
    distance_positive: pd.Series
    distance_negative: pd.Series
    closeness_score: pd.Series
    ranking: pd.Series
    result_table: pd.DataFrame


def calculate_topsis_steps(
    df_input: pd.DataFrame,
    weights: pd.Series,
    criteria_types: dict[str, str] | None = None,
) -> TopsisSteps:
    """Hitung TOPSIS dengan output setiap langkah perhitungan.

    Rumus (skripsi v1 - rumus.pdf):
      R_ij = x_ij / √(Σ x_ij²)
      V_ij = R_ij × W_j
      A⁺: max untuk benefit, min untuk cost
      A⁻: min untuk benefit, max untuk cost
      D⁺ᵢ = √(Σ (V_ij - A⁺ⱼ)²)
      D⁻ᵢ = √(Σ (V_ij - A⁻ⱼ)²)
      Cᵢ* = D⁻ᵢ / (D⁺ᵢ + D⁻ᵢ)
    """
    configure_calculation_logging()

    df = df_input.copy()
    columns = list(df.columns)
    types = criteria_types or {col: CRITERIA_TYPES.get(col, "benefit") for col in columns}

    log_section("METODE TOPSIS — Log Perhitungan Lengkap")
    log_text(f"Jumlah alternatif = {len(df)}")
    log_text(f"Kriteria = {columns}")
    for criterion, kind in types.items():
        log_text(f"  {criterion}: {kind}")

    log_step(
        1,
        "Matriks Keputusan Awal (x_ij)",
        "x_ij dari saham undervalued (ROA, DER, PBV, EPS)",
    )
    log_dataframe("Matriks keputusan D", df)

    log_step(2, "Bobot Entropy (W_j)", "W_j dari hasil perhitungan Entropy")
    for col in columns:
        log_text(
            f"  W[{col}] = {fmt(weights[col])} ({fmt(float(weights[col]) * 100)}%)"
        )
    log_series("Bobot W_j", weights)

    squared = df**2
    squared_sum = np.sum(df.values**2, axis=0)
    norm_factor_values = np.sqrt(squared_sum)
    norm_factor_values = np.where(norm_factor_values == 0, 1e-9, norm_factor_values)
    norm_factor = pd.Series(norm_factor_values, index=columns)

    log_step(3, "Faktor Normalisasi", "√(Σ_i x_ij²) per kriteria")
    for col_idx, col in enumerate(columns):
        parts = " + ".join(fmt(squared.loc[idx, col]) for idx in df.index)
        log_text(f"  Σ x²[{col}] = {parts} = {fmt(squared_sum[col_idx])}")
        log_text(
            f"  √(Σ x²[{col}]) = √({fmt(squared_sum[col_idx])}) = {fmt(norm_factor[col])}"
        )
    log_series("Faktor normalisasi", norm_factor)

    normalized_matrix = df.div(norm_factor, axis=1)
    log_step(4, "Matriks Ternormalisasi Vektor", "R_ij = x_ij / √(Σ_i x_ij²)")
    for idx in df.index:
        for col in columns:
            x_ij = float(df.loc[idx, col])
            denom = float(norm_factor[col])
            r_ij = float(normalized_matrix.loc[idx, col])
            log_text(
                f"  R[{idx},{col}] = {fmt(x_ij)} / {fmt(denom)} = {fmt(r_ij)}"
            )
    log_dataframe("Matriks R_ij", normalized_matrix)

    weighted_matrix = normalized_matrix.mul(weights, axis=1)
    log_step(5, "Matriks Ternormalisasi Terbobot", "V_ij = R_ij × W_j")
    for idx in normalized_matrix.index:
        for col in columns:
            r_ij = float(normalized_matrix.loc[idx, col])
            w_j = float(weights[col])
            v_ij = float(weighted_matrix.loc[idx, col])
            log_text(
                f"  V[{idx},{col}] = {fmt(r_ij)} × {fmt(w_j)} = {fmt(v_ij)}"
            )
    log_dataframe("Matriks V_ij", weighted_matrix)

    ideal_positive_values = []
    ideal_negative_values = []

    log_step(
        6,
        "Solusi Ideal Positif (A⁺)",
        "A⁺ⱼ = max(V_ij) jika benefit; min(V_ij) jika cost",
    )
    for col in columns:
        column_values = weighted_matrix[col].values
        if types[col].lower() == "benefit":
            a_plus = float(np.max(column_values))
            rule = "max"
        else:
            a_plus = float(np.min(column_values))
            rule = "min"
        ideal_positive_values.append(a_plus)
        values_str = ", ".join(fmt(v) for v in column_values)
        log_text(
            f"  A⁺[{col}] = {rule}({values_str}) = {fmt(a_plus)}  [{types[col]}]"
        )

    ideal_positive = pd.Series(ideal_positive_values, index=columns)
    log_series("Hasil A⁺", ideal_positive)

    log_step(
        7,
        "Solusi Ideal Negatif (A⁻)",
        "A⁻ⱼ = min(V_ij) jika benefit; max(V_ij) jika cost",
    )
    for col in columns:
        column_values = weighted_matrix[col].values
        if types[col].lower() == "benefit":
            a_minus = float(np.min(column_values))
            rule = "min"
        else:
            a_minus = float(np.max(column_values))
            rule = "max"
        ideal_negative_values.append(a_minus)
        values_str = ", ".join(fmt(v) for v in column_values)
        log_text(
            f"  A⁻[{col}] = {rule}({values_str}) = {fmt(a_minus)}  [{types[col]}]"
        )

    ideal_negative = pd.Series(ideal_negative_values, index=columns)
    log_series("Hasil A⁻", ideal_negative)

    v_array = weighted_matrix.values
    distance_positive = pd.Series(
        np.sqrt(np.sum((v_array - ideal_positive.values) ** 2, axis=1)),
        index=df.index,
    )
    log_step(8, "Jarak ke Ideal Positif", "D⁺ᵢ = √(Σ_j (V_ij - A⁺ⱼ)²)")
    for row_idx, idx in enumerate(df.index):
        terms = []
        for col_idx, col in enumerate(columns):
            v_ij = float(weighted_matrix.iloc[row_idx, col_idx])
            a_plus = float(ideal_positive[col])
            diff_sq = (v_ij - a_plus) ** 2
            terms.append(f"({fmt(v_ij)} - {fmt(a_plus)})²={fmt(diff_sq)}")
        log_text(f"  D⁺[{idx}] = √({' + '.join(terms)}) = {fmt(distance_positive[idx])}")
    log_series("Hasil D⁺ᵢ", distance_positive)

    distance_negative = pd.Series(
        np.sqrt(np.sum((v_array - ideal_negative.values) ** 2, axis=1)),
        index=df.index,
    )
    log_step(9, "Jarak ke Ideal Negatif", "D⁻ᵢ = √(Σ_j (V_ij - A⁻ⱼ)²)")
    for row_idx, idx in enumerate(df.index):
        terms = []
        for col_idx, col in enumerate(columns):
            v_ij = float(weighted_matrix.iloc[row_idx, col_idx])
            a_minus = float(ideal_negative[col])
            diff_sq = (v_ij - a_minus) ** 2
            terms.append(f"({fmt(v_ij)} - {fmt(a_minus)})²={fmt(diff_sq)}")
        log_text(
            f"  D⁻[{idx}] = √({' + '.join(terms)}) = {fmt(distance_negative[idx])}"
        )
    log_series("Hasil D⁻ᵢ", distance_negative)

    closeness_score = distance_negative / (
        distance_positive + distance_negative + 1e-9
    )
    log_step(10, "Skor Kedekatan Relatif", "Cᵢ* = D⁻ᵢ / (D⁺ᵢ + D⁻ᵢ)")
    for idx in df.index:
        d_plus = float(distance_positive[idx])
        d_minus = float(distance_negative[idx])
        score = float(closeness_score[idx])
        log_text(
            f"  C*[{idx}] = {fmt(d_minus)} / ({fmt(d_plus)} + {fmt(d_minus)}) "
            f"= {fmt(score)}"
        )
    log_series("Hasil Cᵢ*", closeness_score)

    ranking = closeness_score.rank(ascending=False, method="dense").astype(int)
    log_step(11, "Peringkat Akhir", "Rank 1 = Cᵢ* tertinggi")
    for idx in ranking.sort_values().index:
        log_text(
            f"  Rank {int(ranking[idx])}: {idx}  (C* = {fmt(closeness_score[idx])})"
        )

    result_table = df.copy()
    result_table["D_plus"] = distance_positive
    result_table["D_minus"] = distance_negative
    result_table["Skor_TOPSIS"] = closeness_score
    result_table["Rank"] = ranking
    result_table = result_table.sort_values("Rank")

    log_dataframe("Ringkasan hasil TOPSIS", result_table)
    log_text("TOPSIS selesai.")

    return TopsisSteps(
        decision_matrix=df,
        entropy_weights=weights,
        criteria_types=types,
        norm_factor=norm_factor,
        normalized_matrix=normalized_matrix,
        weighted_matrix=weighted_matrix,
        ideal_positive=ideal_positive,
        ideal_negative=ideal_negative,
        distance_positive=distance_positive,
        distance_negative=distance_negative,
        closeness_score=closeness_score,
        ranking=ranking,
        result_table=result_table,
    )


def calculate_topsis(
    df_input: pd.DataFrame,
    weights: pd.Series,
    criteria_types: dict[str, str],
) -> pd.DataFrame:
    """Hitung TOPSIS — kompatibilitas dengan pemanggil lama."""
    return calculate_topsis_steps(df_input, weights, criteria_types).result_table
