import streamlit as st

def Pagina_documentacao():
    """
    Exibe a página de Documentação Técnica na aplicação Streamlit, fornecendo descrições detalhadas 
    dos indicadores financeiros utilizados nas análises de ações.

    Funcionalidades:
        - Apresenta uma introdução à seção de documentação técnica.
        - Explica os indicadores de rentabilidade e suas fórmulas.
        - Explica os indicadores de desconto e suas fórmulas.
        - Explica a Magic Formula e seu conceito.
        - Exibe uma mensagem de atualização contínua da documentação.
        - Fornece referências das fontes utilizadas para compilar as informações.

    Args:
        None

    Returns:
        None
    """
    
    st.title("📚 Documentação Técnica")
    st.markdown("""
    Bem-vindo à seção de Documentação Técnica! Aqui você encontrará informações detalhadas sobre os indicadores utilizados em sua análise de ações.
    ---
    """)

    st.header("📈 Indicadores de Rentabilidade")
    st.markdown("""
    **ROE (Return on Equity)**  
    - Define a eficiência com que uma empresa utiliza os recursos dos acionistas para gerar lucros.
    - Fórmula: `ROE = Lucro Líquido / Patrimônio Líquido`.

    **ROIC (Return on Invested Capital)**  
    - Mede o retorno gerado sobre o capital total investido na empresa.
    - Fórmula: `ROIC = EBIT (1 - Taxa de Imposto) / (Dívida + Patrimônio Líquido)`.

    **ROC (Return on Capital)**  
    - Indica o retorno percentual sobre o capital investido na empresa.
    - Fórmula: `ROC = EBIT / Capital Total`.
    """)

    st.header("💰 Indicadores de Desconto")
    st.markdown("""
    **Earning Yield (Lucro sobre Valor)**  
    - Compara os lucros de uma empresa com seu valor de mercado.
    - Fórmula: `Earning Yield = Lucro por Ação / Preço da Ação`.

    **Dividend Yield (Rendimento de Dividendos)**  
    - Mede a proporção de dividendos pagos em relação ao preço da ação.
    - Fórmula: `Dividend Yield = Dividendos Anuais por Ação / Preço por Ação`.

    **P/VP (Preço sobre Valor Patrimonial)**  
    - Compara o preço de mercado da empresa com seu valor contábil.
    - Fórmula: `P/VP = Preço da Ação / Valor Patrimonial por Ação`.
    """)

    st.header("✨ Magic Formula")
    st.markdown("""
    **Magic Formula** é uma estratégia criada por Joel Greenblatt que combina dois indicadores principais para selecionar ações com potencial de alta rentabilidade e baixo custo:
    
    1️⃣ **Earning Yield (Lucro sobre Valor)**  
    - Mede o lucro operacional da empresa em relação ao valor de mercado.
    
    2️⃣ **ROIC (Return on Invested Capital)**  
    - Avalia a eficiência da empresa em gerar retorno sobre o capital investido.
    
    As empresas são ranqueadas por esses dois indicadores, e a combinação dos rankings resulta em uma lista de ações classificadas como "as melhores para investir" segundo a fórmula.
    """)

    st.markdown("---")
    st.info("💡 Esta página será atualizada constantemente para incluir mais informações relevantes.")

    st.markdown("""
    ---
    **Fontes:**
    - Investopedia ([www.investopedia.com](https://www.investopedia.com))
    - Corporate Finance Institute ([www.corporatefinanceinstitute.com](https://corporatefinanceinstitute.com))
    - Livro: *The Little Book That Still Beats the Market* - Joel Greenblatt
    """)
