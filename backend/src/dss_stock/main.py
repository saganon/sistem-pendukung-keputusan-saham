from pathlib import Path

import yfinance as yf

from dss_stock.entity.stock_info import StockInfo
from dss_stock.graham_formula import GrahamFormula

BASE_DIR = Path(__file__).resolve().parent

file_path = BASE_DIR.parent.parent / "list_stock_code.txt"

with open(file_path, "r", encoding="utf-8") as file:
    content = file.readlines()

for x in content:
    ticker = yf.Ticker(f"{x.strip()}.JK")
    info = ticker.info

    data = StockInfo(
        stock_code=x.strip(),
        market_cap=info.get("marketCap"),
        per=info.get("trailingPE"),
        price_to_book=info.get("priceToBook"),
        return_on_equity=info.get("returnOnEquity"),
        return_on_assets=info.get("returnOnAssets"),
        debt_to_equity=info.get("debtToEquity"),
        current_price=info.get("currentPrice"),
        eps=info.get("trailingEps"),
        bvps=info.get("bookValue"),
    )

    harga_wajar = GrahamFormula.calculate(eps=data.eps, bvps=data.bvps)

    print(harga_wajar)

    print(data)
