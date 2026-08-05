"""
Capítulo 9 — O Cockpit do Atacado
Dashboard interativo com Streamlit + Plotly.
Rodar: streamlit run dashboard.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Painel do Futuro — Atacado São Bento", layout="wide")


@st.cache_data
def load_data():
    datas = pd.date_range("2024-01-01", periods=200, freq="D")
    rcas = ["Ana", "Bruno", "Carla", "David"] * 50
    vendas = np.random.normal(3000, 800, 200).clip(500)
    return pd.DataFrame({"Data": datas, "RCA": rcas, "ValorVenda": vendas})


df = load_data()

st.sidebar.title("Filtros")
data_min, data_max = df["Data"].min().date(), df["Data"].max().date()
d_ini = st.sidebar.date_input("De", data_min, data_min, data_max)
d_fim = st.sidebar.date_input("Até", data_max, data_min, data_max)
rcas_op = ["Todos"] + list(df["RCA"].unique())
rca_sel = st.sidebar.selectbox("RCA", rcas_op)

df_f = df[(df["Data"].dt.date >= d_ini) & (df["Data"].dt.date <= d_fim)]
if rca_sel != "Todos":
    df_f = df_f[df_f["RCA"] == rca_sel]

st.title("Painel do Futuro — Atacado São Bento")

c1, c2, c3 = st.columns(3)
c1.metric("Faturamento", f"R$ {df_f['ValorVenda'].sum():,.0f}")
c2.metric("Pedidos", len(df_f))
c3.metric("Ticket Médio", f"R$ {df_f['ValorVenda'].mean():,.0f}")

st.divider()
col1, col2 = st.columns(2)

with col1:
    vendas_rca = df_f.groupby("RCA")["ValorVenda"].sum().reset_index()
    st.plotly_chart(px.bar(vendas_rca, x="RCA", y="ValorVenda", title="Vendas por RCA"), use_container_width=True)

with col2:
    tend = df_f.groupby("Data")["ValorVenda"].sum().reset_index()
    st.plotly_chart(px.line(tend, x="Data", y="ValorVenda", title="Tendência Diária"), use_container_width=True)
