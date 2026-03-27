from dataclasses import dataclass

@dataclass
class StockInfo:
    stock_code: str
    market_cap: str
    per: str
    price_to_book: str
    return_on_equity: str
    return_on_assets: str
    debt_to_equity: str
    current_price: str
    eps: float
    bvps: float
