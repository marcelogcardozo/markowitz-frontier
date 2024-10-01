import pickle

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

from src import utils

utils.reset_config(st)
utils.set_basic_info(st)

tickers = pickle.load(open("tickers.pkl", "rb"))

available_tickers = tickers

selected_tickers = st.sidebar.multiselect(
    " ",
    available_tickers,
    placeholder="Select the tickers",
    label_visibility="collapsed",
)

tab1, tab2 = st.sidebar.tabs(["Period", "Date Range"])

with tab1:
    selected_period = tab1.selectbox(
        "Select the period",
        ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    )

with tab2:
    min_date = tab2.date_input("Start Date", value=pd.to_datetime("2021-01-01"))
    max_date = tab2.date_input("End Date", value=pd.to_datetime("2021-12-31"))

input_number_of_simulations = st.sidebar.number_input(
    "Number of Simulations", min_value=1, max_value=1000000, value=1000, step=1
)

calculate_button = st.sidebar.button("Calculate")

if calculate_button:
    if len(selected_tickers) == 0:
        st.warning("Please select at least one ticker")

    portfolio = pd.DataFrame()

    if selected_period:
        kwargs = {"period": selected_period}
    else:
        kwargs = {"start": min_date, "end": max_date}

    for ticker in selected_tickers:
        ticker_historical_data = yf.download(ticker, **kwargs)[["Adj Close"]]

        if yf.shared._ERRORS.get(ticker) is not None:
            st.error(f"ERROR: {yf.shared._ERRORS.get(ticker)}")
            selected_tickers.remove(ticker)
            continue

        ticker_historical_data.columns = [ticker]
        portfolio = pd.concat([portfolio, ticker_historical_data], axis=1)

    portfolio.dropna(how="all", axis=1, inplace=True)

    selected_tickers = portfolio.columns.tolist()

    portfolio = portfolio.ffill()
    return_pct = portfolio.pct_change()
    annual_return = return_pct.mean() * 252
    cumulative_return = (return_pct + 1).cumprod() - 1

    annual_cov = return_pct.cov() * 252
    matrix_correlation = return_pct.corr()

    st.markdown("### Portfolio Historical Data Returns")
    st.line_chart(cumulative_return, use_container_width=True)

    col1, col2 = st.columns([0.8, 1.2])

    with col1:
        col1.markdown("### Annual Return")
        df_annual_return = pd.DataFrame(annual_return, columns=["Return"])
        col1.dataframe(
            df_annual_return,
            use_container_width=True,
            column_config={"Return": {"format": "{:.2%}"}},
        )

    with col2:
        col2.markdown("### Correlation Matrix")
        col2.dataframe(matrix_correlation, use_container_width=True)

    number_of_tickers = len(selected_tickers)

    pesos = np.random.random((input_number_of_simulations, number_of_tickers))
    pesos /= pesos.sum(axis=1, keepdims=True)

    lista_retornos = np.dot(pesos, annual_return)
    lista_volatilidade = np.sqrt(np.sum((np.dot(pesos, annual_cov) * pesos), axis=1))
    lista_sharpe_ratio = lista_retornos / lista_volatilidade

    dic_carteiras = {
        "Retorno": lista_retornos,
        "Volatilidade": lista_volatilidade,
        "Sharpe Ratio": lista_sharpe_ratio,
        **{
            acao + " Peso": [Peso[i] for Peso in pesos]
            for i, acao in enumerate(selected_tickers)
        },
    }

    portfolios = pd.DataFrame(dic_carteiras)

    st.markdown("### Simulated Portfolios")
    st.dataframe(portfolios, use_container_width=True)

    st.markdown("### Efficient Frontier")

    lower_volatility = portfolios["Volatilidade"].min()
    higher_volatility = portfolios["Volatilidade"].max()

    lower_volatility_return = portfolios["Retorno"].min()
    higher_volatility_return = portfolios["Retorno"].max()

    xlim = (lower_volatility * 0.9, higher_volatility * 1.1)
    ylim = (lower_volatility_return * 0.9, higher_volatility_return * 1.1)

    c = (
        alt.Chart(portfolios, autosize="fit", height=500)
        .mark_circle()
        .encode(
            x=alt.X("Volatilidade", scale=alt.Scale(domain=xlim)),
            y=alt.Y("Retorno", scale=alt.Scale(domain=ylim)),
            color=alt.Color(
                "Sharpe Ratio", legend=alt.Legend(title="Sharpe Ratio", orient="bottom")
            ),
            tooltip=["Volatilidade", "Retorno", "Sharpe Ratio"],
            description="Sharpe Ratio",
        )
        .configure_axis(grid=False, domain=False)
    )
    st.altair_chart(c, use_container_width=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        col1.markdown("### Minimal Volatility Portfolio")
        min_volatility = portfolios["Volatilidade"].min()
        min_volatility_portfolio = portfolios[
            portfolios["Volatilidade"] == min_volatility
        ].T
        min_volatility_portfolio.columns = ["Value"]
        col1.dataframe(min_volatility_portfolio, use_container_width=True)

    with col2:
        col2.markdown("### Optimal Portfolio")
        max_sharpe = portfolios["Sharpe Ratio"].max()
        max_sharpe_portfolio = portfolios[portfolios["Sharpe Ratio"] == max_sharpe].T
        max_sharpe_portfolio.columns = ["Value"]
        col2.dataframe(max_sharpe_portfolio, use_container_width=True)

    st.markdown("### Backtesting")
    st.markdown("#### Minimal Volatility Portfolio")

    dict_pesos = utils.get_weights_per_ticker(min_volatility_portfolio)
    min_volatility_serie_cumulative_return = utils.get_serie_returns_based_on_weight(
        portfolio.copy(), dict_pesos
    )

    st.line_chart(min_volatility_serie_cumulative_return, use_container_width=True)

    st.markdown("#### Optimal Portfolio")

    dict_pesos = utils.get_weights_per_ticker(max_sharpe_portfolio)
    max_sharpe_serie_cumulative_return = utils.get_serie_returns_based_on_weight(
        portfolio.copy(), dict_pesos
    )

    st.line_chart(max_sharpe_serie_cumulative_return, use_container_width=True)
