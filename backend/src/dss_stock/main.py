from dss_stock.calculate_entropy_weight import calculate_entropy_weights
from dss_stock.under_value_stock import under_value_stock
import pandas as pd

stock_list = under_value_stock()

df = pd.DataFrame([s.__dict__ for s in stock_list])

df['market_cap'] = df['market_cap'].apply(lambda x: f"{x:,.0f}")

print(df.to_string(index=False))

kolom_target = {
    'price_to_book': 'PBV',
    'eps': 'EPS',
    'return_on_assets': 'ROA',
    'debt_to_equity': 'DER'
}

data_saham = df[list(kolom_target.keys())].rename(columns=kolom_target).to_dict(orient='list')
tickers = df['stock_code'].tolist()

df_kriteria = pd.DataFrame(data_saham, index=tickers)

print("--- Matriks Keputusan Awal ---")
print(df_kriteria)
print("\n" + "=" * 50 + "\n")

# 2. Jalankan Fungsi Perhitungan Entropy
bobot_entropy = calculate_entropy_weights(df_kriteria, criteria_types=None)

# 3. Tampilkan Hasil Pretty-Print Bobot Kriteria
print("--- Hasil Bobot Kriteria Menggunakan Metode Entropy ---")
df_hasil = pd.DataFrame(
    {"Nilai Bobot": bobot_entropy, "Persentase": bobot_entropy * 100}
)

# Format tampilan desimal
pd.options.display.float_format = "{:,.4f}".format
df_hasil["Persentase"] = df_hasil["Persentase"].apply(lambda x: f"{x:.2f}%")

print(df_hasil)

# Validasi total bobot harus sama dengan 1
print(f"\nTotal Bobot Kontrol: {bobot_entropy.sum():.2f}")

