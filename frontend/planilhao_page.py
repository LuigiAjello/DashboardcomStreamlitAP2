from backend.routers import menu_planilhao
import streamlit as st 

st.title("Planilhão")
data_base = st.date_input("Digite a data")
df = menu_planilhao(data_base)
st.dataframe(df)



