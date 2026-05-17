from pathlib import Path
import time
import tempfile
import yfinance as yf
from dss_stock.entity.stock_info import StockInfo
from dss_stock.graham_formula import GrahamFormula

# Mengatasi isu cache lokasi timezone pada environment tertentu
try:
    yf.set_tz_cache_location(tempfile.gettempdir())
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent.parent / "list_stock_code.txt"

# Membaca daftar kode saham energi
with open(file_path, "r", encoding="utf-8") as file:
    content = file.readlines()

for x in content:
    stock_code = x.strip()
    if not stock_code:
        continue

    print(f"Processing {stock_code}...")
    ticker = yf.Ticker(f"{stock_code}.JK")

    # Ambil info utama
    info = ticker.info

    current_price = ticker.fast_info.get("last_price")

    if current_price is None:
        current_price = info.get("currentPrice")

    if current_price is None:
        current_price = info.get("previousClose")

    # Jika masih None atau bernilai 0.0, tarik dari data historis
    if current_price is None or (isinstance(current_price, (int, float)) and current_price == 0.0):
        try:
            hist = ticker.history(period="5d")  # Ambil opsi 5 hari untuk antisipasi hari libur
            if not hist.empty:
                current_price = float(hist['Close'].dropna().iloc[-1])
        except Exception as e:
            print(f"Gagal menarik data historis harga untuk {stock_code}: {e}")

    financial_currency = info.get('financialCurrency')
    market_currency = info.get('currency')

    # (yfinance otomatis melakukan auto-convert ke IDR pada properti .info untuk saham IDX)
    raw_eps = info.get("trailingEps")
    raw_bvps = info.get("bookValue")

    # Jika di .info bernilai None, baru intip financials / balance_sheet
    try:
        if raw_eps is None:
            financials = ticker.financials
            if not financials.empty and "Diluted EPS" in financials.index:
                raw_eps = financials.loc["Diluted EPS"].iloc[0]

        if raw_bvps is None:
            balance_sheet = ticker.balance_sheet
            if not balance_sheet.empty and "Stockholders Equity" in balance_sheet.index and "Ordinary Shares Number" in balance_sheet.index:
                total_equity = balance_sheet.loc["Stockholders Equity"].iloc[0]
                total_shares = balance_sheet.loc["Ordinary Shares Number"].iloc[0]
                raw_bvps = total_equity / total_shares
    except Exception as e:
        print(f"Data komponen backup bermasalah untuk {stock_code}: {e}")

    # 3. Sinkronisasi ke Objek Model Data
    data = StockInfo(
        stock_code=stock_code,
        market_cap=info.get("marketCap"),
        per=info.get("trailingPE"),
        price_to_book=info.get("priceToBook"),
        return_on_equity=info.get("returnOnEquity"),
        return_on_assets=info.get("returnOnAssets"),
        debt_to_equity=info.get("debtToEquity"),
        current_price=current_price,
        eps=raw_eps,
        bvps=raw_bvps,
        currency=market_currency if market_currency else 'Data tidak tersedia'
    )

    # 4. Validasi Perhitungan Formula Graham
    if data.eps is None or data.bvps is None:
        print(f"Skipping stock {data.stock_code}: Missing EPS or BVPS data.")
        harga_wajar = 0.0
    elif data.eps <= 0 or data.bvps <= 0:
        print(f"Skipping stock {data.stock_code}: Graham Formula is not applicable for negative EPS or BVPS.")
        harga_wajar = 0.0
    else:
        harga_wajar = GrahamFormula.calculate(eps=data.eps, bvps=data.bvps)

    # 5. Logika Keputusan Evaluasi Akhir
    if data.current_price is None:
        print(f"Skipping decision for {data.stock_code}: Missing current market price data setelah jaring pengaman historis.")
    elif harga_wajar > data.current_price:
        print(f"UNDERVALUE {data.stock_code} | Price: {data.current_price} | Harga Wajar: {harga_wajar:.2f} | Mata Uang Laporan Keuangan: {financial_currency} | Mata Uang Pasar (Saham): {market_currency}")
    else:
        print(f"OVERVALUE {data.stock_code} | Price: {data.current_price} | Harga Wajar: {harga_wajar:.2f} | Mata Uang Laporan Keuangan: {financial_currency} | Mata Uang Pasar (Saham): {market_currency}")

    print("-" * 40)

    # 6. Time Delay (Krusial: Mencegah rate-limit/blokir IP oleh Yahoo Finance)
    time.sleep(1.5)