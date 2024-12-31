import streamlit as st
import pandas as pd

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
def carregar_base ():
  file_path = "Bases/Planilha de Movimentação.xlsx"

  base_acoes = pd.read_excel(file_path,sheet_name = "Ações")
  base_rf = pd.read_excel(file_path,sheet_name = "Renda Fixa")
  base_fundos = pd.read_excel(file_path,sheet_name = "Fundos")

  dic_base = {
      "Ações":base_acoes,
      "Renda Fixa":base_rf,
      "Fundos":base_fundos
  }  
  return dic_base

selecionar_ativo = st.pills(
    "Selecione o Ativo",
    options=["Fundos","Ações","Renda Fixa"],
    selection_mode="single",
    default="Fundos"
)

base_selecionada = bases[selecionar_ativo]

if selecionar_ativo == "Fundos":
  coluna_de_data = "Data Operação"
else:
  coluna_de_data = "Data"

seletor_1,seletor_2 = st.columns(2)

with seletor_1:

  today = datetime.now()
  last_month = today - timedelta(days=30)

  data_seletor = st.date_input(
        "Selecione a data",
        (last_month, today),
        format="DD/MM/YYYY",
    )

if len(data_seletor) > 1:
  start_date, end_date = data_seletor
else:
  start_date = data_seletor[0]
  end_date = start_date

filtered_df = base_selecionada.loc[(base_selecionada[coluna_de_data] >= pd.Timestamp(start_date)) & (base_selecionada[coluna_de_data] <= pd.Timestamp(end_date))]

with seletor_2:

  carteiras = sorted(filtered_df["Carteira"].unique())

  selecionar_carteira = st.selectbox("Selecione a carteira",carteiras)
  filtered_df = filtered_df.loc[filtered_df["Carteira"] == selecionar_carteira]

st.dataframe(bases[selection],hide_index = True,use_container_width = True)

