import yfinance as yf

file_path = "../../list_stock_code.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.readlines()

for x in content:
    ticker = yf.Ticker(f"{x.strip()}.JK")
    info = ticker.info

    data = {
        "Kode Saham": x.strip(),
        "Market Cap": info.get("marketCap"),
        "PER (Trailing)": info.get("trailingPE"),
        "PER (Forward)": info.get("forwardPE"),
        "PBV": info.get("priceToBook"),
        "ROE": info.get("returnOnEquity"),
        "ROA": info.get("returnOnAssets"),
        "DER": info.get("debtToEquity"),
    }
    print(data)
