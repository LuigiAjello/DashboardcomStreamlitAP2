import streamlit as st
import pandas as pd
from datetime import date
from backend.views import carteira, validar_data
from backend.routers import menu_estrategia
from log_config.logging_config import logger  # Importa o logger centralizado

def Pagina_estrategia():
    """
    Exibe a página de estratégia na aplicação Streamlit, permitindo ao usuário selecionar indicadores financeiros
    e parâmetros para gerar uma carteira de ações.

    Funcionalidades:
        - Permite a escolha de indicadores de rentabilidade e desconto.
        - Permite a seleção de uma data base para análise e o número de ações desejadas.
        - Gera uma carteira de ações com base nos critérios selecionados.
        - Exibe os resultados da análise em formato tabular.

    Args:
        None

    Returns:
        None
    """
    try:
        logger.info("Página Estratégia carregada.")
        
        # Título e descrição
        st.title("🔍 Estratégia de Seleção de Ações")
        st.caption("""
        Utilize indicadores financeiros de rentabilidade e desconto para identificar oportunidades de mercado.
        ---
        """)

        # Dicionários para mapeamento dos rótulos amigáveis para valores técnicos
        indicadores_rentabilidade = {
            "ROE (Return on Equity)": "roe",
            "ROIC (Return on Invested Capital)": "roic",
            "ROC (Return on Capital)": "roc",
        }

        indicadores_desconto = {
            "Earning Yield (Lucro sobre Valor)": "earning_yield",
            "Dividend Yield (Rendimento de Dividendos)": "dividend_yield",
            "P/VP (Preço sobre Valor Patrimonial)": "p_vp",
        }

        # Inputs para seleção dos indicadores
        st.markdown("### 📈 Escolha os Indicadores")
        indicador_rent = st.selectbox(
            "Selecione o indicador de **rentabilidade**:",
            options=list(indicadores_rentabilidade.keys())
        )
        indicador_rent_valor = indicadores_rentabilidade[indicador_rent]
        logger.info(f"Indicador de rentabilidade selecionado: {indicador_rent} ({indicador_rent_valor})")

        indicador_desc = st.selectbox(
            "Selecione o indicador de **desconto**:",
            options=list(indicadores_desconto.keys())
        )
        indicador_desc_valor = indicadores_desconto[indicador_desc]
        logger.info(f"Indicador de desconto selecionado: {indicador_desc} ({indicador_desc_valor})")

        # Input de data e quantidade de ações
        st.markdown("### 🗓️ Selecione o Período e Quantidade de Ações")
        data = st.date_input("Escolha uma data base:", value=pd.to_datetime('today'))
        num = st.number_input(
            "Quantas ações você deseja analisar?",
            min_value=1, max_value=3000, value=10
        )
        logger.info(f"Data selecionada: {data}. Quantidade de ações: {num}")

        # Validação da data
        validar_data(data)

        # Buscar os dados ao clicar no botão
        if st.button("Gerar Estratégia"):
            logger.info("Usuário clicou em 'Gerar Estratégia'.")
            try:
                # Geração da carteira de ações
                df_sorted, acoes_carteira = carteira(data, indicador_rent_valor, indicador_desc_valor, num)

                # Armazenar no session_state
                st.session_state.acoes_carteira = acoes_carteira
                st.session_state.df_sorted = df_sorted
                st.session_state.estrategia_preenchida = True
                logger.info(f"Carteira gerada com sucesso. Ações selecionadas: {acoes_carteira}")

                # Exibição dos resultados
                st.markdown("### 📊 Resultados da Análise")
                st.write(
                    f"Top {num} ações pelo indicador de rentabilidade: **{indicador_rent}** e "
                    f"pelo indicador de desconto **{indicador_desc}** com base na data **{data.strftime('%Y-%m-%d')}**."
                )
                st.dataframe(df_sorted)
                st.success("✅ Estratégia gerada com sucesso!")
            except Exception as e:
                logger.error(f"Erro ao gerar estratégia: {e}")
                st.error("❌ Ocorreu um erro ao gerar a estratégia. Por favor, tente novamente.")
    except Exception as e:
        logger.error(f"Erro na página Estratégia: {e}")
        st.error("❌ Ocorreu um erro inesperado. Verifique os logs ou entre em contato com o suporte.")
