import pandas as pd

from dss_stock.calculate_entropy_weight import EntropySteps
from dss_stock.calculate_topsis import CRITERIA_TYPES, TopsisSteps, calculate_topsis_steps
from dss_stock.entity.stock_info import StockInfo

TOPSIS_FORMULAS = {
    "decision_matrix": "Matriks keputusan ROA, DER, PBV, EPS (saham undervalued)",
    "entropy_weights": "Bobot W_j dari hasil perhitungan Entropy",
    "norm_factor": "√(Σ x_ij²) per kriteria",
    "normalized_matrix": "R_ij = x_ij / √(Σ x_ij²)",
    "weighted_matrix": "V_ij = R_ij × W_j",
    "ideal_positive": "A⁺: max (benefit), min (cost)",
    "ideal_negative": "A⁻: min (benefit), max (cost)",
    "distance_positive": "D⁺ᵢ = √(Σ (V_ij - A⁺ⱼ)²)",
    "distance_negative": "D⁻ᵢ = √(Σ (V_ij - A⁻ⱼ)²)",
    "closeness_score": "Cᵢ* = D⁻ᵢ / (D⁺ᵢ + D⁻ᵢ)",
    "ranking": "Peringkat berdasarkan Cᵢ* tertinggi = rank 1",
}


def run_topsis_analysis(
    undervalued_stocks: list[StockInfo],
    entropy_steps: EntropySteps,
) -> TopsisSteps:
    decision_matrix = entropy_steps.decision_matrix
    return calculate_topsis_steps(
        df_input=decision_matrix,
        weights=entropy_steps.weights,
        criteria_types=CRITERIA_TYPES,
    )


def print_topsis_tables(steps: TopsisSteps) -> None:
    pd.options.display.float_format = "{:,.6f}".format
    pd.options.display.max_columns = None
    pd.options.display.width = None

    print("\n=== METODE TOPSIS — Rumus per Langkah ===")
    for step_name, formula in TOPSIS_FORMULAS.items():
        print(f"  {step_name}: {formula}")

    print("\nJenis kriteria:")
    for criterion, kind in steps.criteria_types.items():
        print(f"  {criterion}: {kind}")

    print("\n--- Langkah 1: Matriks Keputusan Awal (x_ij) ---")
    print(steps.decision_matrix.to_string())

    print("\n--- Langkah 2: Bobot Entropy (W_j) ---")
    weights_table = pd.DataFrame(
        {
            "kriteria": steps.entropy_weights.index,
            "bobot_wj": steps.entropy_weights.values,
            "bobot_persen": steps.entropy_weights.values * 100,
        }
    )
    print(weights_table.to_string(index=False))

    print("\n--- Langkah 3: Faktor Normalisasi √(Σ x_ij²) per Kriteria ---")
    print(steps.norm_factor.to_string())

    print("\n--- Langkah 4: Matriks Ternormalisasi Vektor (R_ij = x_ij / √(Σ x_ij²)) ---")
    print(steps.normalized_matrix.to_string())

    print("\n--- Langkah 5: Matriks Ternormalisasi Terbobot (V_ij = R_ij × W_j) ---")
    print(steps.weighted_matrix.to_string())

    print("\n--- Langkah 6: Solusi Ideal Positif (A⁺) ---")
    print(steps.ideal_positive.to_string())

    print("\n--- Langkah 7: Solusi Ideal Negatif (A⁻) ---")
    print(steps.ideal_negative.to_string())

    print("\n--- Langkah 8: Jarak ke Solusi Ideal Positif (D⁺ᵢ) ---")
    print(steps.distance_positive.to_string())

    print("\n--- Langkah 9: Jarak ke Solusi Ideal Negatif (D⁻ᵢ) ---")
    print(steps.distance_negative.to_string())

    print("\n--- Langkah 10: Skor Kedekatan Relatif (Cᵢ* = D⁻ᵢ / (D⁺ᵢ + D⁻ᵢ)) ---")
    score_table = pd.DataFrame(
        {
            "saham": steps.closeness_score.index,
            "D_plus": steps.distance_positive.values,
            "D_minus": steps.distance_negative.values,
            "skor_topsis": steps.closeness_score.values,
        }
    )
    print(score_table.to_string(index=False))

    print("\n--- Langkah 11: Peringkat Akhir TOPSIS ---")
    rank_table = pd.DataFrame(
        {
            "saham": steps.ranking.sort_values().index,
            "rank": steps.ranking.sort_values().values,
            "skor_topsis": steps.closeness_score.loc[
                steps.ranking.sort_values().index
            ].values,
        }
    ).sort_values("rank")
    print(rank_table.to_string(index=False))

    print("\n--- Ringkasan Lengkap ---")
    summary_cols = ["D_plus", "D_minus", "Skor_TOPSIS", "Rank"]
    print(steps.result_table[summary_cols].to_string())
