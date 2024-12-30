import streamlit as st
import pandas as pd

#Criação da página
st.set_page_config(page_title="Movimentações de Clientes", page_icon="💰", layout="wide")

#Declarar funcao para otimização da página

@st.cache_data
def carregar_base ():
  base_acoes = pd.read_excel("Bases/Planilha de Movimentação.xlsx",sheet_name = "Ações")
  base_rf = pd.read_excel("Bases/Planilha de Movimentação.xlsx",sheet_name = "Renda Fixa")
  base_fundos = pd.read_excel("Bases/Planilha de Movimentação.xlsx",sheet_name = "Fundos")

  dic_base = {"Ações":base_acoes, "Renda Fixa":base_rf, "Fundos":base_fundos}  
  return dic_base

selection = st.pills(
    "Tipo de Operação",options = ["Ações","Fundos","Renda Fixa"],
    selection_mode="single",
    default = "Ações"
)

st.title("Operações-teste")
bases = carregar_base ()
st.dataframe(bases[selection],hide_index = True,use_container_width = True)

