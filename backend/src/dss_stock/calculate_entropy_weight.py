import numpy as np
import pandas as pd


def calculate_entropy_weights(df_input):
    """Menghitung bobot kriteria menggunakan metode Entropy.

    Parameters:
    - df_input: pandas DataFrame (baris = alternatif/saham, kolom = kriteria)
    - criteria_types: dict, contoh {'PER': 'cost', 'ROE': 'benefit'}
                      (Opsional jika normalisasi Anda bergantung pada jenis
                      kriteria)

    Returns:
    - weights_series: pandas Series berisi bobot final tiap kriteria
    """
    # Buat copy agar tidak merusak dataframe asli
    df = df_input.copy()

    # 1. NORMALISASI MATRIKS KEPUTUSAN (p_ij)
    # Rumus: p_ij = x_ij / sum(x_ij) untuk setiap kolom
    # Kita tambahkan epsilon (1e-9) untuk menghindari pembagian dengan nol jika ada kolom bernilai 0
    p_matrix = df.apply(lambda x: x / (x.sum() + 1e-9), axis=0)

    # 2. MENGHITUNG NILAI ENTROPY (E_j)
    # Rumus: E_j = -k * sum(p_ij * ln(p_ij))
    # di mana k = 1 / ln(n) dan n = jumlah alternatif (baris)
    n = len(df)
    k = 1.0 / np.log(n)

    entropy_j = []
    for col in p_matrix.columns:
        # Ambil kolom p_ij
        p_ij = p_matrix[col]

        # Saring nilai p_ij yang bernilai 0, karena ln(0) tidak terdefinisi (NaN)
        # Gunakan np.where untuk memberikan nilai 0 jika p_ij <= 0
        log_p_ij = np.where(p_ij > 0, np.log(p_ij), 0.0)

        # Hitung sum(p_ij * ln(p_ij))
        sum_p_log_p = np.sum(p_ij * log_p_ij)

        # Hitung E_j
        E_j = -k * sum_p_log_p
        entropy_j.append(E_j)

    entropy_series = pd.Series(entropy_j, index=df.columns)

    # 3. MENGHITUNG TINGKAT DIVERSIFIKASI (d_j)
    # Rumus: d_j = 1 - E_j
    div_series = 1.0 - entropy_series

    # 4. MENGHITUNG BOBOT ENTROPY FINAL (w_j)
    # Rumus: w_j = d_j / sum(d_j)
    weights_series = div_series / div_series.sum()

    return weights_series
