import pickle

import pandas as pd
from requests import get


def reset_config(st) -> None:
    def _get_footer():
        style = """
            <style>
                # MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .stApp { bottom: 0px; }
            </style>
        """
        return style

    st.set_page_config(
        page_title="Efficient Frontier",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            "Get Help": "mailto:marcelo.cardozo.cg@gmail.com?subject=Ajuda%20-%20Calculadora%20de%20Tensão%20Crítica",
            "Report a bug": "mailto:marcelo.cardozo.cg@gmail.com?subject=BUG%20-%20Calculadora%20de%20Tensão%20Crítica",
        },
    )

    st.markdown(_get_footer(), unsafe_allow_html=True)


def set_basic_info(st) -> None:
    st.title("Markowitz Portfolio Optimization")
    st.markdown("""
    Feito por: Marcelo Cardozo  &bull; [GitHub](https://github.com/marcelogcardozo)
                                &bull; [LinkedIn](https://www.linkedin.com/in/marcelogcardozo/)

    Versão: 1.0
    """)

    st.markdown(
        """
        <style>
        img {
            width: 25px; /* Define a largura da imagem */
            height: 25px; /* Define a altura da imagem */
            border-radius: 50%; /* Cria um efeito de círculo */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Resultados")
    st.divider()


def get_tickers() -> list:
    url = "https://www.dadosdemercado.com.br/bolsa/acoes"

    r = get(url)
    r.raise_for_status()

    df = pd.read_html(r.text)[0]
    df.sort_values(by="Ticker", ascending=True, inplace=True)

    tickers = [ticker + ".SA" for ticker in df["Ticker"].unique().tolist()]

    with open("tickers.pkl", "wb") as f:
        pickle.dump(tickers, f)

    return tickers


def get_weights_per_ticker(portfolio: pd.DataFrame) -> dict:
    dict_pesos = {
        col.split(" Peso")[0]: portfolio.loc[col, "Value"]
        for col in portfolio.index
        if "Peso" in col
    }

    return dict_pesos


def get_serie_returns_based_on_weight(
    portfolio: pd.DataFrame, dict_pesos: dict
) -> pd.DataFrame:
    for ticker in dict_pesos.keys():
        portfolio[ticker] = portfolio[ticker] * dict_pesos[ticker]

    portfolio = portfolio.sum(axis=1)
    portfolio = portfolio / portfolio.iloc[0]

    return_serie = portfolio.pct_change()
    cumulative_return = (return_serie + 1).cumprod() - 1

    return cumulative_return
