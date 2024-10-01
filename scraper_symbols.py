import pickle

import pandas as pd
from requests import get

url = "https://www.dadosdemercado.com.br/bolsa/acoes"

r = get(url)
r.raise_for_status()

df = pd.read_html(r.text)[0]
df.sort_values(by="Ticker", ascending=True, inplace=True)

tickers = [ticker + ".SA" for ticker in df["Ticker"].unique().tolist()]

with open("tickers.pkl", "wb") as f:
    pickle.dump(tickers, f)
