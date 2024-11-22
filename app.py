import streamlit as st
import logging

# Configurar o logger
from log_config.logging_config import logger  # Importa o logger centralizado

# Importar páginas
from frontend.planilhao_page import Pagina_planilhao
from frontend.estrategia_page import Pagina_estrategia
from frontend.grafico_page import Pagina_grafico
from frontend.Pagina_inicio import Pagina_inicio
from frontend.documentacao_page import Pagina_documentacao

# Configurar o estado inicial
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "INÍCIO"
    logger.debug("Estado inicial 'pagina_atual' definido para 'INÍCIO'.")
if "estrategia_preenchida" not in st.session_state:
    st.session_state.estrategia_preenchida = False
    logger.debug("Estado inicial 'estrategia_preenchida' definido para False.")
if "acoes_carteira" not in st.session_state:
    st.session_state.acoes_carteira = None
    logger.debug("Estado inicial 'acoes_carteira' definido para None.")

# Estilizar os botões com CSS para ficarem vermelhos
st.markdown("""
<style>
/* Estilo base para o botão */
div.stButton > button:first-child {
    background-color: #ff4d4d !important; /* Cor vermelha */
    color: white !important;
    border: none !important;
    width: 150px !important;
    height: 50px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border-radius: 5px !important;
    cursor: pointer !important;
    transition: background-color 0.3s ease !important;
}

/* Estado hover */
div.stButton > button:first-child:hover {
    background-color: #e60000 !important; /* Vermelho mais escuro ao passar o mouse */
    color: white !important;
}

/* Estado ativo (quando o botão é clicado) */
div.stButton > button:first-child:active {
    background-color: #cc0000 !important; /* Vermelho ainda mais escuro ao clicar */
    color: white !important;
}

/* Estado de foco (após o botão ser clicado) */
div.stButton > button:first-child:focus:not(:focus-visible) {
    outline: none !important; /* Remove o contorno ao focar */
}

/* Opcional: Remove quaisquer estilos de foco padrão */
div.stButton > button:focus {
    box-shadow: none !important;
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

# Conteúdo dos botões no corpo principal
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🏠 Início"):
            logger.info("Botão 'Início' clicado.")
            st.session_state.pagina_atual = "INÍCIO"
    with col2:
        if st.button("📋 Planilhão"):
            logger.info("Botão 'Planilhão' clicado.")
            st.session_state.pagina_atual = "PLANILHÃO"
    with col3:
        if st.button("🔍 Estratégia"):
            logger.info("Botão 'Estratégia' clicado.")
            st.session_state.pagina_atual = "ESTRATÉGIA"
    with col4:
        if st.button("📊 Gráfico"):
            logger.info("Botão 'Gráfico' clicado.")
            st.session_state.pagina_atual = "GRÁFICO"
    with col5:
        if st.button("📚 Documentação"):
            logger.info("Botão 'Documentação' clicado.")
            st.session_state.pagina_atual = "DOCUMENTAÇÃO"

def renderizar_pagina():
    """
    Renderiza a página atual com base no estado da sessão.
    """
    logger.debug(f"Renderizando a página: {st.session_state.pagina_atual}")
    if st.session_state.pagina_atual == "INÍCIO":
        Pagina_inicio()
    elif st.session_state.pagina_atual == "PLANILHÃO":
        Pagina_planilhao()
    elif st.session_state.pagina_atual == "ESTRATÉGIA":
        Pagina_estrategia()
        if "acoes_carteira" in st.session_state and st.session_state.acoes_carteira is not None:
            st.session_state.estrategia_preenchida = True
            logger.info("Estratégia preenchida com sucesso.")
    elif st.session_state.pagina_atual == "GRÁFICO":
        if not st.session_state.get("estrategia_preenchida", False):
            logger.warning("Tentativa de acessar Gráfico sem preencher Estratégia.")
            with st.spinner("Esperando estratégia..."):
                st.error("Você precisa preencher a Estratégia antes de acessar os Gráficos.")
        else:
            logger.info("Acessando a página de Gráfico.")
            Pagina_grafico(restrict_access=False)
    elif st.session_state.pagina_atual == "DOCUMENTAÇÃO":
        Pagina_documentacao()
    else:
        logger.error(f"Página desconhecida: {st.session_state.pagina_atual}")
        st.error("Página não encontrada.")

# Renderizar a página
renderizar_pagina()
