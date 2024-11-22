import streamlit as st
import pandas as pd
from backend.views import pegar_df_preco_corrigido, pegar_df_preco_diversos, validar_data
from backend.routers import Comparacao_graficos
from log_config.logging_config import logger  # Importa o logger centralizado

def Pagina_grafico(restrict_access=False):
    """
    Exibe a página de gráficos na aplicação Streamlit, permitindo ao usuário analisar 
    e comparar os retornos acumulados da carteira de ações com o IBOVESPA.

    Funcionalidades:
        - Verifica se a estratégia está preenchida antes de continuar.
        - Permite ao usuário selecionar um período de análise com datas de início e fim.
        - Gera gráficos comparativos do retorno acumulado da carteira e do IBOVESPA.
        - Valida as datas selecionadas pelo usuário.

    Args:
        restrict_access (bool, optional): Flag para restringir o acesso à página. Padrão é False.

    Returns:
        None
    """
    logger.info("Página Gráficos carregada.")  # Registro de carregamento da página
    
    # Título sempre visível
    st.title("📊 Análise de Gráficos")
    st.caption("""
    Bem-vindo à seção de **Gráficos**! Aqui você pode visualizar e comparar a variação dos retornos acumulados da sua carteira de ações com o IBOVESPA.  
    Escolha o período desejado para realizar uma análise detalhada.
    ---
    """)

    if not st.session_state.get("estrategia_preenchida", False):
        logger.warning("A estratégia não foi preenchida.")
        with st.spinner("⏳ Esperando estratégia..."):
            st.error("❌ Você precisa preencher a Estratégia antes de acessar os Gráficos.")
            st.info("➡️ Vá até a aba **Estratégia** para configurar sua carteira de ações.")
        return

    logger.info("Estratégia preenchida. Continuando para análise de gráficos.")
    
    acoes_carteira = st.session_state.acoes_carteira
    if acoes_carteira is None:
        logger.error("Ações da carteira não foram configuradas.")
        st.error("⚠️ Nenhuma carteira foi gerada. Por favor, configure sua estratégia antes de acessar os gráficos.")
        return

    st.markdown("### 📅 Selecione o Período de Análise")
    data_inicio_fim = st.date_input(
        "Escolha as datas de início e fim para análise:",
        value=(pd.to_datetime('today'), pd.to_datetime('today')),
        key="data_periodo"
    )

    if len(data_inicio_fim) == 2:
        data_ini, data_fim = data_inicio_fim
        try:
            validar_data(data_ini)
            validar_data(data_fim)
            logger.info(f"Período selecionado: {data_ini} - {data_fim}")

            if data_ini > data_fim:
                logger.warning("Data de fim é anterior à data de início.")
                st.error("⚠️ A data de fim deve ser posterior à data de início.")
                return

            if st.button("Gerar Gráficos"):
                try:
                    df_carteira = pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira)
                    df_ibov = pegar_df_preco_diversos(data_ini, data_fim)
                    logger.info("Gráficos gerados com sucesso.")
                    st.subheader("📊 Comparativo: Retorno Acumulado Carteira x IBOVESPA")
                    Comparacao_graficos(df_carteira, df_ibov)
                    st.success("✅ Gráficos gerados com sucesso!")
                except Exception as e:
                    logger.error(f"Erro ao gerar gráficos: {e}")
                    st.error(f"❌ Erro ao gerar gráficos: {e}")
        except Exception as e:
            logger.error(f"Erro ao processar as datas: {e}")
            st.error(f"❌ Erro ao processar as datas: {e}")
