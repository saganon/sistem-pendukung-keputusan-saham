from dss_stock.normalize_data import under_value_stock
import pandas as pd

stock_list = under_value_stock()

df = pd.DataFrame([s.__dict__ for s in stock_list])

pd.options.display.float_format = '{:,.2f}'.format
df['market_cap'] = df['market_cap'].apply(lambda x: f"{x:,.0f}")

print(df.to_string(index=False))