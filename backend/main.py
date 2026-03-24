import yfinance as yf

ticker = yf.Ticker("BBCA.JK")
info = ticker.info

data = {
    "Market Cap": info.get("marketCap"),
    "PER (Trailing)": info.get("trailingPE"),
    "PER (Forward)": info.get("forwardPE"),
    "PBV": info.get("priceToBook"),
    "ROE": info.get("returnOnEquity"),
    "ROA": info.get("returnOnAssets"),
    "DER": info.get("debtToEquity")
}

print(data)