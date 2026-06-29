from dataclasses import dataclass

import numpy as np
import pandas as pd

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
    df = df_input.copy()
    columns = list(df.columns)
    types = criteria_types or {col: CRITERIA_TYPES.get(col, "benefit") for col in columns}

    w = np.array([weights[col] for col in columns])

    squared_sum = np.sum(df.values**2, axis=0)
    norm_factor_values = np.sqrt(squared_sum)
    norm_factor_values = np.where(norm_factor_values == 0, 1e-9, norm_factor_values)
    norm_factor = pd.Series(norm_factor_values, index=columns)

    normalized_matrix = df.div(norm_factor, axis=1)
    weighted_matrix = normalized_matrix.mul(weights, axis=1)

    ideal_positive_values = []
    ideal_negative_values = []

    for col in columns:
        column_values = weighted_matrix[col].values
        if types[col].lower() == "benefit":
            ideal_positive_values.append(np.max(column_values))
            ideal_negative_values.append(np.min(column_values))
        else:
            ideal_positive_values.append(np.min(column_values))
            ideal_negative_values.append(np.max(column_values))

    ideal_positive = pd.Series(ideal_positive_values, index=columns)
    ideal_negative = pd.Series(ideal_negative_values, index=columns)

    v_array = weighted_matrix.values
    distance_positive = pd.Series(
        np.sqrt(np.sum((v_array - ideal_positive.values) ** 2, axis=1)),
        index=df.index,
    )
    distance_negative = pd.Series(
        np.sqrt(np.sum((v_array - ideal_negative.values) ** 2, axis=1)),
        index=df.index,
    )

    closeness_score = distance_negative / (
        distance_positive + distance_negative + 1e-9
    )
    ranking = closeness_score.rank(ascending=False, method="dense").astype(int)

    result_table = df.copy()
    result_table["D_plus"] = distance_positive
    result_table["D_minus"] = distance_negative
    result_table["Skor_TOPSIS"] = closeness_score
    result_table["Rank"] = ranking
    result_table = result_table.sort_values("Rank")

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
