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
def carregar_bases ():
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

bases_df = carregar_bases()

colunas_1,colunas_2,coluna_3 = st.columns(3)

with colunas_1:

  seletor_de_abas = st.pills("Selecione o Ativo",options=["Fundos","Ações","Renda Fixa"],selection_mode="single",default="Fundos")

with colunas_2:

  base_selecionado_df = bases_df[seletor_de_abas]
  carteiras_unicas = base_selecionado_df["Carteira"].unique()
  selecionar_carteira = st.multiselect("Selecione a carteira",carteiras_unicas)

with coluna_3:

  today = datetime.now()
  la_atras = today - timedelta(days=1800)

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


total_financeiro = base_filtrada["Financeiro"].sum()
st.metric(label="Total Financeiro", value=f"R$ {total_financeiro}")

st.dataframe(bases[selection],hide_index = True,use_container_width = True)

