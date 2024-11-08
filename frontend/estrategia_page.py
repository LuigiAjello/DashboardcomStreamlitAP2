import streamlit as st
from datetime import date
from backend.views import carteira  # Importando a função carteira de views.py

def selecionar_data():
    # Input de data única
    data_selecionada = st.date_input(
        "Selecione a data:",
        value=date.today(),  # Valor padrão para hoje
    )

    # Retorna a data selecionada
    if data_selecionada:
        return data_selecionada
    else:
        st.write("Por favor, selecione uma data.")
        return None

def selecionar_numero_acoes():
    # Input numérico para selecionar o número de ações na carteira
    numero_acoes = st.number_input(
        "Selecione o número de ações na carteira:",
        min_value=1,
        step=1,
        format="%d"
    )
    return numero_acoes



# Título da aplicação
st.title("Estratégia")

# Inputs de seleção
ind_Rentabilidade = st.selectbox("Selecione Indicador de Rentabilidade:", ["roc", "roe", "roic"])
ind_Desconto = st.selectbox("Selecione Indicador de Desconto:", ["earning_yield", "dividend_yield", "p_vp"])

# Input de data e número de ações
data_base = selecionar_data()
numero_acoes = selecionar_numero_acoes()

# Botão para pegar informações e executar uma ação
if st.button("Run"):
    # Executar ação com base nos inputs selecionados
    if data_base and numero_acoes > 0:
        # Executa a função `carteira` com os parâmetros selecionados
        tickers_selecionados = carteira(data_base, ind_Rentabilidade, ind_Desconto, numero_acoes)
        st.write("Tickers Selecionados:", tickers_selecionados)
    else:
        st.write("Por favor, verifique se todos os campos estão preenchidos corretamente.")
