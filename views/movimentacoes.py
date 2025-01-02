import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#Criação da página
st.set_page_config(page_title="Movimentações de Clientes", page_icon="💰", layout="wide")

#Inserção do logo e alinhamento de colunas
header_1, header_2 = st.columns([1,3])

with header_1:

  st.image("Imagens/logo.png")

with header_2:

  st.title("Controle de Movimentação 2")

#Declarar funcao para otimização da página

@st.cache_data()
def carregar_bases ():
  file_path = "Bases/Planilha de Movimentação.xlsx"

  base_acoes = pd.read_excel(file_path,sheet_name = "Ações")
  base_rf = pd.read_excel(file_path,sheet_name = "Renda Fixa")
  base_fundos = pd.read_excel(file_path,sheet_name = "Fundos")

  # Garantir que as colunas de data sejam do tipo datetime
  if "Data Operação" in base_fundos.columns:
    base_fundos["Data Operação"] = pd.to_datetime(base_fundos["Data Operação"])

  if "Data Conversão" in base_fundos.columns:
    base_fundos["Data Conversão"] = pd.to_datetime(base_fundos["Data Conversão"])

  if "Data Liquidação" in base_fundos.columns:
    base_fundos["Data Liquidação"] = pd.to_datetime(base_fundos["Data Liquidação"])

  if "Data" in base_acoes.columns:
    base_acoes["Data"] = pd.to_datetime(base_acoes["Data"])

  if "Data" in base_rf.columns:
    base_rf["Data"] = pd.to_datetime(base_rf["Data"])

  dic_base = {
      "Ações":base_acoes,
      "Renda Fixa":base_rf,
      "Fundos":base_fundos
  }
  return dic_base

bases_df = carregar_bases()

colunas_1,colunas_2,coluna_3 = st.columns(3)

with colunas_1:

  seletor_de_abas = st.pills("Selecione o Ativo",options=["Fundos","Ações","Renda Fixa"],selection_mode="single",default="Fundos")
  
# Verificar se o ativo selecionado existe no dicionário
  if seletor_de_abas in bases_df:
    base_selecionado_df = bases_df[seletor_de_abas]
  else:
    st.error(f"O ativo selecionado '{seletor_de_abas}' não foi encontrado nas bases disponíveis.")
    st.stop()  # Interrompe a execução caso o valor seja inválido

with colunas_2:

  base_selecionado_df = bases_df[seletor_de_abas]
  carteiras_unicas = base_selecionado_df["Carteira"].unique()
  selecionar_carteira = st.multiselect("Selecione a carteira",carteiras_unicas)

with coluna_3:

  today = datetime.now()
  la_atras = today - timedelta(days=365)

  data_seletor = st.date_input(
        "Selecione a data",
        (la_atras, today),
        format="DD/MM/YYYY",
    )


if len(selecionar_carteira) == 0:
  base_filtrada = base_selecionado_df
else:
  base_filtrada = base_selecionado_df.loc[base_selecionado_df["Carteira"].isin(selecionar_carteira)]

if len(data_seletor) == 0:
  pass
else:
  if len(data_seletor) == 2:
    start_date, end_date = data_seletor
  else:
    start_date = data_seletor[0]
    end_date = start_date

  if seletor_de_abas == "Fundos":
    coluna_de_data = "Data Operação"
  else:
    coluna_de_data = "Data"

  base_filtrada = base_filtrada.loc[(base_filtrada[coluna_de_data] >= pd.Timestamp(start_date)) & (base_filtrada[coluna_de_data] <= pd.Timestamp(end_date))]


#total_financeiro = base_filtrada["Financeiro"].sum()
#st.metric(label="Total Financeiro", value=f"R$ {total_financeiro}")

if "Data Operação" in base_filtrada.columns:
    base_filtrada["Data Operação"] = base_filtrada["Data Operação"].dt.strftime('%d/%m/%Y')

if "Data Conversão" in base_filtrada.columns:
    base_filtrada["Data Conversão"] = base_filtrada["Data Conversão"].dt.strftime('%d/%m/%Y')

if "Data Liquidação" in base_filtrada.columns:
    base_filtrada["Data Liquidação"] = base_filtrada["Data Liquidação"].dt.strftime('%d/%m/%Y')

if "Data" in base_filtrada.columns:
    base_filtrada["Data"] = base_filtrada["Data"].dt.strftime('%d/%m/%Y')

st.dataframe(base_filtrada,hide_index=True,use_container_width=True)
