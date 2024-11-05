import os
import requests
from dotenv import load_dotenv

# Carregar o token do arquivo .env
load_dotenv()
token = os.getenv('TOKEN')
headers = {'Authorization': f'JWT {token}'}

import logging
logger = logging.getLogger(__name__)

def pegar_planilhao(data_base):
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    dados (list): lista com o dicionario com todas as Ações.
    """
    params = {'data_base': data_base}
    try:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
        if r.status_code == 200:
            dados = r.json()
            logger.info(f"Dados do Planilhao consultados com sucesso: {data_base}")
            print(f"Dados do Planilhao consultados com sucesso: {data_base}")
            return dados
        else:
           logger.error(f"Erro na consulta do planilhao: {data_base}")
           print((f"Erro na consulta do planilhao: {data_base}"))
    except Exception as e:
        logger.error(f"ERRO TECNICO{e}")
        print(f"Erro na funcao consultar_planilhao: {e}")

dados_planilhao = pegar_planilhao("2023-04-03")
