import numpy as np
import pandas as pd


def calculate_entropy_weights(df_input):
    df = df_input.copy()
    columns = df.columns

    # m merepresentasikan jumlah keseluruhan emiten yang masuk (baris dataframe)
    m = len(df)

    # =========================================================================
    # 1. NORMALISASI PROPORSI (P_ij)
    # Rumus Tesis: P_ij = C_ij / sqrt( sum( C_ij^2 ) )
    # =========================================================================
    # Menghitung akar kuadrat dari jumlah kuadrat keseluruhan nilai per kriteria
    norm_factor = np.sqrt(np.sum(df.values**2, axis=0))

    # Jaring pengaman anti-pembagian nol
    norm_factor = np.where(norm_factor == 0, 1e-9, norm_factor)

    # Matriks Proposional P
    P = df.values / norm_factor

    # =========================================================================
    # 2. MENGHITUNG NILAI ENTROPY (E_j)
    # Rumus Tesis: k = 1 / ln(m)  dan  E_j = -k * sum( P_ij * ln(P_ij) )
    # =========================================================================
    k = 1.0 / np.log(m)

    entropy_j = []
    for idx, _col in enumerate(columns):
        P_ij = P[:, idx]

        # Jaring pengaman: ln(x) tidak terdefinisi jika x <= 0.
        # Jika nilai P_ij <= 0, kita set hasil log-nya ke 0.0 agar tidak menghasilkan NaN.
        log_P_ij = np.where(P_ij > 0, np.log(P_ij), 0.0)

        # Akumulasi perkalian P_ij * ln(P_ij) untuk seluruh alternatif
        sum_p_log_p = np.sum(P_ij * log_P_ij)

        # E_j = -k * total akumulasi
        E_j = -k * sum_p_log_p
        entropy_j.append(E_j)

    entropy_series = pd.Series(entropy_j, index=columns)

    # =========================================================================
    # 3. DERAJAT KERAGAMAN (d_j)
    # Rumus Tesis: d_j = 1 - E_j
    # =========================================================================
    div_series = 1.0 - entropy_series

    # =========================================================================
    # 4. BOBOT FINAL (W_j)
    # Rumus Tesis: W_j = d_j / sum( d_j )
    # =========================================================================
    weights_series = div_series / div_series.sum()

    return weights_series
