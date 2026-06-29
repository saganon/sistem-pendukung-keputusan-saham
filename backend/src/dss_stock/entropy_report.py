import pandas as pd

from dss_stock.calculate_entropy_weight import (
    CRITERIA_COLUMNS,
    EntropySteps,
    build_decision_matrix,
    calculate_entropy_steps,
)
from dss_stock.entity.stock_info import StockInfo

ENTROPY_FORMULAS = {
    "decision_matrix": "Matriks awal: ROA, DER, PBV, EPS dari data yfinance",
    "proportion_matrix": "p_ij = x_ij / Σ x_ij  (normalisasi proporsi per kolom)",
    "ln_proportion_matrix": "ln(p_ij), jika p_ij = 0 maka 0",
    "p_times_ln_p_matrix": "p_ij × ln(p_ij)",
    "sum_p_ln_p": "Σ (p_ij × ln(p_ij)) per kriteria",
    "k_constant": "k = 1 / ln(n),  n = jumlah saham undervalued",
    "entropy": "E_j = -k × Σ (p_ij × ln(p_ij))",
    "diversification": "d_j = 1 - E_j",
    "weights": "w_j = d_j / Σ d_j",
}


def run_entropy_analysis(
    undervalued_stocks: list[StockInfo],
) -> tuple[pd.DataFrame, EntropySteps]:
    decision_matrix = build_decision_matrix(undervalued_stocks)
    steps = calculate_entropy_steps(decision_matrix)
    return decision_matrix, steps


def print_entropy_tables(steps: EntropySteps) -> None:
    pd.options.display.float_format = "{:,.6f}".format
    pd.options.display.max_columns = None
    pd.options.display.width = None

    print("\n=== METODE ENTROPY — Rumus per Langkah ===")
    for step_name, formula in ENTROPY_FORMULAS.items():
        print(f"  {step_name}: {formula}")

    print("\n--- Langkah 1: Matriks Keputusan Awal (D) ---")
    print("Kriteria: ROA (%), DER, PBV, EPS — hanya saham undervalued")
    print(steps.decision_matrix.to_string())

    print("\n--- Langkah 2: Total per Kriteria (Σ x_ij) ---")
    print(steps.column_totals.to_string())

    print("\n--- Langkah 3: Normalisasi Proporsi (p_ij = x_ij / Σ x_ij) ---")
    print(steps.proportion_matrix.to_string())

    print("\n--- Langkah 4: ln(p_ij) ---")
    print(steps.ln_proportion_matrix.to_string())

    print("\n--- Langkah 5: p_ij × ln(p_ij) ---")
    print(steps.p_times_ln_p_matrix.to_string())

    print("\n--- Langkah 6: Σ (p_ij × ln(p_ij)) per Kriteria ---")
    print(steps.sum_p_ln_p.to_string())

    print("\n--- Langkah 7: Konstanta k = 1 / ln(n) ---")
    print(f"n (jumlah alternatif) = {steps.n_alternatives}")
    print(f"k = {steps.k_constant:.6f}")

    print("\n--- Langkah 8: Nilai Entropy (E_j = -k × Σ p_ij ln p_ij) ---")
    print(steps.entropy.to_string())

    print("\n--- Langkah 9: Tingkat Diversifikasi (d_j = 1 - E_j) ---")
    print(steps.diversification.to_string())

    print("\n--- Langkah 10: Bobot Entropy Final (w_j = d_j / Σ d_j) ---")
    weights_table = pd.DataFrame(
        {
            "kriteria": steps.weights.index,
            "entropy_Ej": steps.entropy.values,
            "diversifikasi_dj": steps.diversification.values,
            "bobot_wj": steps.weights.values,
            "bobot_persen": steps.weights.values * 100,
        }
    )
    print(weights_table.to_string(index=False))
