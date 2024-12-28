import streamlit as st

# --- PAGE SETUP ---
movimentacoes = st.Page(
    "views/movimentacoes.py",
    title="Página 1",
    icon=":material/savings:",
    default=True
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "movimentacoes": [movimentacoes]
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("assets/codingisfun_logo.png")

# --- RUN NAVIGATION ---
pg.run()
