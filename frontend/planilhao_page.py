import streamlit as st
from backend.routers import menu_planilhao
from backend.views import validar_data
from log_config.logging_config import logger  # Importa o logger centralizado

def Pagina_planilhao():
    try:
        logger.info("Página Planilhão carregada.")
        
        # Título e descrição
        st.title("📋 Visão Geral dos Dados de Mercado")
        st.caption("""
        Bem-vindo ao **Planilhão**! Aqui você pode explorar dados de mercado detalhados, filtrados por data.  
        Use esta ferramenta para acessar informações relevantes e tomar decisões informadas com base nos dados mais recentes.
        ---
        """)

        # Entrada de data
        st.markdown("### 🗓️ Selecione a Data de Análise")
        data_base = st.date_input("Escolha uma data base para buscar os dados:")
        logger.info(f"Data selecionada: {data_base}")

        # Validação da data
        validar_data(data_base)

        # Ação ao clicar no botão "Buscar"
        if st.button("🔍 Buscar Dados"):
            logger.info(f"Usuário clicou em 'Buscar' para a data: {data_base}")
            try:
                # Consulta os dados
                df = menu_planilhao(data_base)
                if not df.empty:
                    # Exibe o DataFrame no Streamlit
                    st.markdown("### 📊 Resultados da Análise")
                    st.dataframe(df, height=600, use_container_width=True)
                    st.success(f"✅ Dados encontrados! Total de {len(df)} registros exibidos.")
                    logger.info(f"Dados encontrados: {len(df)} linhas exibidas.")
                else:
                    # Caso nenhum dado seja encontrado
                    st.warning("⚠️ Nenhum dado foi encontrado para a data selecionada. Tente outra data!")
                    logger.warning(f"Nenhum dado encontrado para a data: {data_base}")
            except Exception as e:
                logger.error(f"Erro ao buscar dados do Planilhão para a data: {data_base} | {e}")
                st.error("❌ Ocorreu um erro ao buscar os dados. Por favor, tente novamente.")
    except Exception as e:
        logger.error(f"Erro na página Planilhão: {e}")
        st.error("❌ Ocorreu um erro inesperado. Verifique os logs ou entre em contato com o suporte.")
