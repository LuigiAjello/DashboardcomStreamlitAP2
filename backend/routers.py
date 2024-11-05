import streamlit as st
from backend.views import pegar_df_planilhao

def menu_planilhao(data_base):
    df = pegar_df_planilhao(data_base)
    return df 

