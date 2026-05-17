from dss_stock.calculate_entropy_weight import calculate_entropy_weights
from dss_stock.calculate_topsis import calculate_topsis
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

bobot_entropy = calculate_entropy_weights(df_kriteria)

jenis_kriteria = {
    "PBV": "cost",
    "EPS": "benefit",
    "ROA": "benefit",
    "DER": "cost",
}

hasil_topsis = calculate_topsis(df_kriteria, bobot_entropy, jenis_kriteria)

print("--- Hasil Perankingan Akhir Menggunakan Metode TOPSIS ---")
pd.options.display.float_format = "{:,.4f}".format
print(hasil_topsis[["D_plus", "D_minus", "Skor_TOPSIS", "Rank"]])