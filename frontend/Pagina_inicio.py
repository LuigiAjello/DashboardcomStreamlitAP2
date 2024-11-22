import streamlit as st

def Pagina_inicio():
    """
    Exibe a página inicial da aplicação Streamlit, fornecendo uma introdução à plataforma
    e orientações sobre como utilizá-la.

    Funcionalidades:
        - Apresentação do título e introdução da plataforma.
        - Orientações de como começar a usar as funcionalidades disponíveis.
        - Agradecimentos à equipe de desenvolvimento.
        - Informações de contato do responsável.
        - Configuração inicial do estado da sessão.

    Args:
        None

    Returns:
        None
    """
    # Título com emoji
    st.title("Bem-vindo ao Minha Carteira Minha Vida 📈")
    
    # Texto de introdução com estilo
    st.markdown("""
    ### 🌐 Sua plataforma para gerenciar carteiras de ações
    Aqui você pode:
    - 🧮 **Analisar e criar estratégias personalizadas para suas ações.**
    - 📊 **Visualizar gráficos interativos e comparativos de desempenho.**
    - 📈 **Tomar decisões mais informadas e eficazes no mercado financeiro.**
    """)

    # Seção de como começar
    st.markdown("""
    ---
    ## 🚀 Como Começar
    1️⃣ **Acesse a aba [Estratégia]** para gerar sua carteira de ações com os melhores indicadores.  
    2️⃣ **Depois, explore a aba [Gráficos]** para analisar visualmente o desempenho das suas escolhas.  
    3️⃣ **Confira a aba [Documentação]** para entender os indicadores usados em suas análises.  
    """)

    # Seção de agradecimentos
    st.markdown("""
    ---
    ## 🎓 Equipe de Desenvolvimento
    Esta plataforma foi desenvolvida com dedicação pelos seguintes alunos:  
    - **Luigi Ajello**  
    - **Isabella Aguiar**  
    - **Milton Rodrigues**  
    """)

    # Seção de contato
    st.markdown("""
    ---
    ## 📩 Contato
    - **Email:** [luigipedrosoajello@gmail.com](mailto:luigipedrosoajello@gmail.com)  
    - **LinkedIn:** [www.linkedin.com/in/luigi-pedroso-ajello-346934278](https://www.linkedin.com/in/luigi-pedroso-ajello-346934278)  
    - **GitHub:** [https://github.com/LuigiAjello](https://github.com/LuigiAjello)  
    """)

    # Configurando o estado inicial
    if "pagina_atual" not in st.session_state:
        st.session_state.pagina_atual = "inicio"
