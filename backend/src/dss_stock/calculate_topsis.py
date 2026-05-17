import numpy as np


def calculate_topsis(df_input, weights, criteria_types):
    """

    Parameters:
    - df_input: pandas DataFrame (baris = alternatif/saham, kolom = kriteria)
    - weights: pandas Series atau dict berisi bobot kriteria hasil Entropy
    - criteria_types: dict berisi jenis kriteria, contoh: {'PER': 'cost',
    'ROE': 'benefit'}

    """
    df = df_input.copy()
    columns = df.columns

    # Pastikan bobot berbentuk numpy array yang urutannya sesuai dengan kolom df
    w = np.array([weights[col] for col in columns])

    # =========================================================================
    # 1. NORMALISASI MATRIKS (R_ij)
    # Rumus: R_ij = C_ij / sqrt(sum(x_ij^2))
    # =========================================================================
    # Menghitung akar kuadrat dari jumlah kuadrat keseluruhan nilai per kriteria
    norm_factor = np.sqrt(np.sum(df.values**2, axis=0))

    # Menghindari pembagian dengan nol (zero division) jika ada kolom bernilai 0
    norm_factor = np.where(norm_factor == 0, 1e-9, norm_factor)

    # Matriks Ternormalisasi R
    R = df.values / norm_factor

    # =========================================================================
    # 2. NORMALISASI TERBOBOT (V_ij)
    # Rumus: V_ij = R_ij * W_j
    # =========================================================================
    V = R * w

    # =========================================================================
    # 3. MENENTUKAN SOLUSI IDEAL (A+ dan A-)
    # =========================================================================
    A_positive = []
    A_negative = []

    for idx, col in enumerate(columns):
        c_type = criteria_types[col].lower()

        if c_type == "benefit":
            # A+ mengambil nilai tertinggi, A- mengambil nilai terendah
            A_positive.append(np.max(V[:, idx]))
            A_negative.append(np.min(V[:, idx]))
        elif c_type == "cost":
            # A+ mengambil nilai terendah, A- mengambil nilai tertinggi
            A_positive.append(np.min(V[:, idx]))
            A_negative.append(np.max(V[:, idx]))

    A_positive = np.array(A_positive)
    A_negative = np.array(A_negative)

    # =========================================================================
    # 4. MENGHITUNG JARAK EUCLIDEAN (D_i+ dan D_i-)
    # Rumus: D_i = sqrt(sum((V_ij - A_j)^2))
    # =========================================================================
    # Menggunakan np.tile atau broadcasting untuk menghitung selisih jarak
    D_positive = np.sqrt(np.sum((V - A_positive) ** 2, axis=1))
    D_negative = np.sqrt(np.sum((V - A_negative) ** 2, axis=1))

    # =========================================================================
    # 5. SKOR FINAL (C_i*) DAN PERANKINGAN
    # Rumus: C_i* = D_negative / (D_positive + D_negative)
    # =========================================================================
    # Tambahkan epsilon kecil untuk menghindari pembagian 0 jika D+ dan D- bernilai 0
    closeness_score = D_negative / (D_positive + D_negative + 1e-9)

    # Masukkan hasil kalkulasi ke dalam DataFrame hasil
    df_result = df_input.copy()
    df_result["D_plus"] = D_positive
    df_result["D_minus"] = D_negative
    df_result["Skor_TOPSIS"] = closeness_score

    # Menghitung Ranking (skor tertinggi mendapatkan peringkat 1)
    df_result["Rank"] = (
        df_result["Skor_TOPSIS"].rank(ascending=False, method="dense").astype(int)
    )

    # Urutkan DataFrame berdasarkan peringkat terbaik
    df_result = df_result.sort_values(by="Rank")

    return df_result
