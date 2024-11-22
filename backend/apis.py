import os
import requests
from dotenv import load_dotenv
from log_config.logging_config import logger  # Importa o logger centralizado

# Carregar o token do arquivo .env
load_dotenv()
token = os.getenv('TOKEN')

if not token:
    logger.error("TOKEN não encontrado no arquivo .env.")
    raise ValueError("TOKEN não encontrado no arquivo .env.")

headers = {'Authorization': f'JWT {token}'}
logger.info("Token carregado com sucesso.")

def pegar_planilhao(data_base):
    """
    Consulta o endpoint do planilhão para obter dados com base em uma data específica.

    Args:
        data_base (str): Data base para a consulta ao planilhão no formato 'YYYY-MM-DD'.

    Returns:
        dict or None: Dados retornados pela API em formato JSON, ou None em caso de erro.
    """
    logger.info(f"Iniciando consulta ao planilhão para a data base: {data_base}")
    params = {'data_base': data_base}
    try:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao', params=params, headers=headers)
        if r.status_code == 200:
            dados = r.json()
            logger.info(f"Consulta ao planilhão bem-sucedida para a data base: {data_base}")
            return dados
        else:
            logger.warning(f"Erro ao consultar o planilhão: {data_base} | Status Code: {r.status_code} | Response: {r.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"Erro técnico ao consultar o planilhão: {data_base} | {e}")
        return None


def get_preco_corrigido(ticker, data_ini, data_fim):
    """
    Consulta o endpoint para obter os preços corrigidos de uma ação em um período especificado.

    Args:
        ticker (str): Ticker da ação a ser consultada.
        data_ini (str): Data inicial do período no formato 'YYYY-MM-DD'.
        data_fim (str): Data final do período no formato 'YYYY-MM-DD'.

    Returns:
        dict or None: Dados retornados pela API em formato JSON, ou None em caso de erro.
    """
    logger.info(f"Iniciando consulta de preço corrigido para {ticker} de {data_ini} a {data_fim}.")
    params = {'ticker': ticker, 'data_ini': data_ini, 'data_fim': data_fim}
    try:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido', params=params, headers=headers)
        if r.status_code == 200:
            preco_corrigido = r.json()
            logger.info(f"Consulta de preço corrigido bem-sucedida para {ticker}.")
            return preco_corrigido
        else:
            logger.warning(f"Falha na consulta de preço corrigido para {ticker} | Status Code: {r.status_code} | Response: {r.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"Erro técnico ao consultar preço corrigido para {ticker}: {e}")
        return None


def get_preco_diversos(data_ini, data_fim, ticker):
    """
    Consulta o endpoint para obter os preços diversos de uma ação em um período especificado.

    Args:
        data_ini (str): Data inicial do período no formato 'YYYY-MM-DD'.
        data_fim (str): Data final do período no formato 'YYYY-MM-DD'.
        ticker (str): Ticker da ação a ser consultada.

    Returns:
        dict or None: Dados retornados pela API em formato JSON, ou None em caso de erro.
    """
    logger.info(f"Iniciando consulta de preços diversos para {ticker} de {data_ini} a {data_fim}.")
    params_ibov = {'ticker': ticker, 'data_ini': data_ini, 'data_fim': data_fim}
    try:
        r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params_ibov, headers=headers)
        if r.status_code == 200:
            response_ibov = r.json()
            logger.info(f"Consulta de preços diversos bem-sucedida para {ticker}.")
            return response_ibov
        else:
            logger.warning(f"Falha na consulta de preços diversos para {ticker} | Status Code: {r.status_code} | Response: {r.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"Erro técnico ao consultar preços diversos para {ticker}: {e}")
        return None
