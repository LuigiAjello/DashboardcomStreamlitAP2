import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path
import pandas as pd
import streamlit as st

# Importar páginas
from frontend.planilhao_page import Pagina_planilhao
from frontend.estrategia_page import Pagina_estrategia
from frontend.grafico_page import Pagina_grafico
from frontend.Pagina_inicio import Pagina_inicio
from frontend.documentacao_page import Pagina_documentacao

# Configurar o estado inicial
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "INÍCIO"
if "estrategia_preenchida" not in st.session_state:
    st.session_state.estrategia_preenchida = False
if "acoes_carteira" not in st.session_state:
    st.session_state.acoes_carteira = None

# Estilizar a barra lateral e os botões com CSS
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #f0f8ff;
    padding: 20px;
    border-right: 2px solid #007bff;
}
.sidebar .sidebar-content h2 {
    color: #007bff;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}
.sidebar .sidebar-content button {
    background-color: #007bff;
    color: white;
    border: none;
    width: 100%;
    height: 60px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 5px;
    margin-bottom: 15px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
}
.sidebar .sidebar-content button:hover {
    background-color: #0056b3;
    color: white;
}
.sidebar .sidebar-content button.active {
    background-color: #0056b3;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Conteúdo do Sidebar
with st.sidebar:
    st.markdown("<h2>Minha Carteira Minha Vida 📊</h2>", unsafe_allow_html=True)
    if st.button("🏠 Início", key="inicio"):
        st.session_state.pagina_atual = "INÍCIO"
    if st.button("📋 Planilhão", key="planilhao"):
        st.session_state.pagina_atual = "PLANILHÃO"
    if st.button("🔍 Estratégia", key="estrategia"):
        st.session_state.pagina_atual = "ESTRATÉGIA"
    if st.button("📊 Gráfico", key="grafico"):
        st.session_state.pagina_atual = "GRÁFICO"
    if st.button("📚 Documentação", key="documentacao"):
        st.session_state.pagina_atual = "DOCUMENTAÇÃO"

# Função para renderizar a página com verificação de estado
def renderizar_pagina():
    if st.session_state.pagina_atual == "INÍCIO":
        Pagina_inicio()
    elif st.session_state.pagina_atual == "PLANILHÃO":
        Pagina_planilhao()
    elif st.session_state.pagina_atual == "ESTRATÉGIA":
        # Atualiza estado após preencher estratégia
        Pagina_estrategia()
        if "acoes_carteira" in st.session_state and st.session_state.acoes_carteira is not None:
            st.session_state.estrategia_preenchida = True
    elif st.session_state.pagina_atual == "GRÁFICO":
        # Verificar se a estratégia foi preenchida
        if not st.session_state.get("estrategia_preenchida", False):
            with st.spinner("Esperando estratégia..."):
                st.error("Você precisa preencher a Estratégia antes de acessar os Gráficos.")
        else:
            Pagina_grafico(restrict_access=False)
    elif st.session_state.pagina_atual == "DOCUMENTAÇÃO":
        Pagina_documentacao()

# Renderizar a página
renderizar_pagina()
