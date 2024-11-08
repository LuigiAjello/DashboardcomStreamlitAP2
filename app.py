import sys
import os
from pathlib import Path
import streamlit as st
import setup_paths
from backend.routers import menu_planilhao

# Configuração do diretório base
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(BASE_DIR))


planilhao_page = st.Page("frontend/planilhao_page.py",title="Planilhao", default=True)
estrategia_page = st.Page("frontend/estrategia_page.py",title="Estrategia")
graficos_page = st.Page("frontend/graficos_page.py",title="Graficos")

pg = st.navigation(
    {
        "Planilhao":[planilhao_page],
        "Estrategia":[estrategia_page],
        "Graficos": [graficos_page],
    }
)
pg.run()