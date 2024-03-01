import pandas as pd

def get_weights_per_ticker(portfolio: pd.DataFrame) -> dict:
    
    dict_pesos = {col.split(' Peso')[0]: portfolio.loc[col, 'Value'] 
              for col in portfolio.index if 'Peso' in col}

    return dict_pesos

def get_serie_returns_based_on_weight(portfolio: pd.DataFrame, dict_pesos: dict) -> pd.DataFrame:
    
    for ticker in dict_pesos.keys():
        portfolio[ticker] = portfolio[ticker] * dict_pesos[ticker]
    
    portfolio = portfolio.sum(axis=1)
    portfolio = portfolio / portfolio.iloc[0]

    return_serie = portfolio.pct_change()
    cumulative_return = (return_serie + 1).cumprod() - 1

    return cumulative_return
    
