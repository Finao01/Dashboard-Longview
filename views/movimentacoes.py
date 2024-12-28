import streamlit as st
import pandas as pd

st.set_page_config(page_title="Movimentações de Clientes", page_icon="💰", layout="wide")

selection = st.pills(
    "Tipo de Operação",options = ["Ações","Fundos","Renda Fixa"],
    selection_mode="single",
)

st.title("Operações")
base_df = pd.read_excel("Bases/Planilha de Movimentação.xlsx",selection)
st.dataframe(base_df)

