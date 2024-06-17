# import
import yfinance as yf
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os

# import das variaveis de ambiente

commodities = [
    "CL=F",
    "GC=F",
    "SI=F",
]  # CL=F => Crude Oil; GC=F => Gold; SI=F => Silver

# Carregando variaveis de ambiente

load_dotenv()

DB_HOST = os.getenv("DB_HOST_PROD")
DB_PORT = os.getenv("DB_PORT_PROD")
DB_NAME = os.getenv("DB_NAME_PROD")
DB_USER = os.getenv("DB_USER_PROD")
DB_PASS = os.getenv("DB_PASS_PROD")
DB_SCHEMA = os.getenv("DB_SCHEMA_PROD")


# Fazendo URL de conexão
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def buscar_dados_commodities(simbolo, periodo="5d", intervalo="1d"):
    ticker = yf.Ticker("CL=F")
    dados = ticker.history(period=periodo, interval=intervalo)[
        ["Close"]
    ]  # retorna um dataframe
    dados["simbolo"] = simbolo
    return dados


def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)


def salvar_no_postgres(df, schema="public"):
    df.to_sql(
        "commodities",
        engine,
        if_exists="replace",
        index=True,
        index_label="Date",
        schema=schema,
    )


if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados, schema="public")


# pegar a cotacao dos meus ativos
