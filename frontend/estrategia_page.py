import streamlit as st

def selecionar_periodo():
    # Input de data sem valor padrão, permitindo seleção de intervalo
    data_selecionada = st.date_input(
        "Selecione o período:",
        value=(),
    )

    # Verificar se o usuário selecionou um intervalo válido
    if len(data_selecionada) == 2:
        data_inicio_selecionada, data_fim_selecionada = data_selecionada
        st.write("Data de início:", data_inicio_selecionada)
        st.write("Data de fim:", data_fim_selecionada)
        return data_inicio_selecionada, data_fim_selecionada
    elif len(data_selecionada) == 1:
        st.write("Selecione uma data final para completar o intervalo.")
        return None, None
    else:
        st.write("Por favor, selecione uma data ou um intervalo de datas.")
        return None, None

def selecionar_numero_acoes():
    # Input numérico para selecionar o número de ações na carteira
    numero_acoes = st.number_input(
        "Selecione o número de ações na carteira:",
        min_value=0,
        step=1,
        format="%d"
    )
    return numero_acoes

# Título da aplicação
st.title("Estratégia")

# Inputs de seleção
ind_Rentabilidade = st.selectbox("Selecione Indicador de Rentabilidade:", ["ROE", "ROC", "ROIC"])
ind_Desconto = st.selectbox("Selecione Indicador de Desconto:", ["Earning Yield", "Dividend Yield", "P-B"])

# Inputs de data e número de ações
data_inicio, data_fim = selecionar_periodo()
numero_acoes = selecionar_numero_acoes()

# Botão para pegar informações e executar uma ação
if st.button("Run"):
    # Executar ação com base nos inputs selecionados
    if data_inicio and data_fim:
        st.write("Executando com os seguintes parâmetros:")
        st.write("Indicador de Rentabilidade:", ind_Rentabilidade)
        st.write("Indicador de Desconto:", ind_Desconto)
        st.write("Período de:", data_inicio, "a", data_fim)
        st.write("Número de ações na carteira:", numero_acoes)
        
        # Aqui você pode adicionar o código para executar o processamento adicional
        st.write("Processamento adicional em execução...")
    else:
        st.write("Por favor, selecione um intervalo de datas válido. ")



