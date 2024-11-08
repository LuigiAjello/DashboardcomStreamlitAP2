import pandas as pd
from datetime import date
import logging
logger = logging.getLogger(__name__)
from backend.apis import (pegar_planilhao)

def filtrar_duplicado(df:pd.DataFrame, meio:str = None) -> pd.DataFrame:
    """
    Filtra o df das ações duplicados baseado no meio escolhido (defau

    params:
    df (pd.DataFrame): dataframe com os ticker duplicados 
    meio (str): campo escolhido para escolher qual ticker escolher (default: volume)

    return:
    (pd.DataFrame): dataframe com os ticker filtrados.
    """
    meio = meio or 'volume'
    df_dup = df[df.empresa.duplicated(keep=False)]
    lst_dup = df_dup.empresa.unique()
    lst_final = []
    for tic in lst_dup:
        tic_dup = df_dup[df_dup.empresa==tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]
        lst_final = lst_final + [tic_dup]
    lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values
    logger.info(f"Ticker Duplicados Filtrados: {lst_dup}")
    print(f"Ticker Duplicados Filtrados: {lst_dup}")
    return df[~df.ticker.isin(lst_dup)]

def pegar_df_planilhao(data_base:date) -> pd.DataFrame:
    """
    Consulta todas as ações com os principais indicadores fundamentalistas

    params:
    data_base (date): Data Base para o cálculo dos indicadores.

    return:
    df (pd.DataFrame): DataFrame com todas as Ações.
    """
    dados = pegar_planilhao(data_base)
    if dados:
        dados = dados['dados']
        planilhao = pd.DataFrame(dados)
        planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]
        df = filtrar_duplicado(planilhao)
        logger.info(f"Dados do Planilhao consultados com sucesso: {data_base}")
        print(f"Dados do Planilhao consultados com sucesso: {data_base}")
        return df
    else:
        logger.info(f"Sem Dados no Planilhão: {data_base}")
        print(f"Sem Dados no Planilhão: {data_base}")

def carteira(data, crit_rentabilidade, crit_desconto, num_acoes):
    # Extrai o DataFrame com os dados financeiros
    df = pegar_df_planilhao(data)
    colunas_relevantes = ["ticker", "setor", "data_base", "roc", "roe", "roic", "earning_yield", "dividend_yield", "p_vp"]
    df = df[colunas_relevantes]
    
    # Seleção com base na rentabilidade (usando todas as ações disponíveis)
    df_rentabilidade = df.nlargest(len(df), crit_rentabilidade).reset_index(drop=True)
    df_rentabilidade['rank_rentabilidade'] = df_rentabilidade.index  # Ranking baseado na rentabilidade
    
    # Seleção com base no desconto (ajustando a seleção para o critério 'p_vp')
    if crit_desconto == "p_vp":
        df_desconto = df.nsmallest(len(df), crit_desconto).reset_index(drop=True)
    else:
        df_desconto = df.nlargest(len(df), crit_desconto).reset_index(drop=True)
    df_desconto['rank_desconto'] = df_desconto.index  # Ranking baseado no desconto
    
    # Combinação dos DataFrames e cálculo da média dos rankings
    df_combinado = pd.merge(df_desconto[["ticker", "rank_desconto"]], 
                            df_rentabilidade[["ticker", "rank_rentabilidade"]], 
                            on="ticker", 
                            how="inner")
    df_combinado["pontuacao_media"] = (df_combinado["rank_desconto"] + df_combinado["rank_rentabilidade"]) / 2
    
    # Ordenação e seleção das melhores ações com ranking iniciado em 1
    df_ordenado = df_combinado.sort_values(by=['pontuacao_media'], ascending=True).reset_index(drop=True)
    df_ordenado['ranking'] = df_ordenado.index + 1  # Adiciona ranking começando em 1
    
    # Seleção dos tickers com base no número desejado de ações
    df_final = df_ordenado.nsmallest(num_acoes, 'pontuacao_media').reset_index(drop=True)
    
    # Retorna apenas os tickers selecionados
    return df_final['ticker']



def pegar_df_preco_corrigido(data_ini:date, data_fim:date, carteira:list) -> pd.DataFrame:
    """
    Consulta os preços Corrigidos de uma lista de ações

    params:
    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    for ticker in carteira:
        dados = get_preco_corrigido(data_ini, data_fim, ticker)
        if dados:
            dados = dados.json()['dados']
            df_temp = pd.DataFrame.from_dict(dados)
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')   
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco

def pegar_df_preco_diversos(data_ini:date, data_fim:date, carteira:list) -> pd.DataFrame:
    """
    Consulta os preços históricos de uma carteira de ativos

    params:

    data_ini (date): data inicial da consulta
    data_fim (date): data final da consulta
    carteira (list): lista de ativos a serem consultados

    return:
    df_preco (pd.DataFrame): dataframe com os preços do período dos ativos da lista
    """
    df_preco = pd.DataFrame()
    for ticker in carteira:
        dados = get_preco_diversos(data_ini, data_fim, ticker)
        if dados:
            dados = dados.json()['dados']
            df_temp = pd.DataFrame.from_dict(dados)
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
            logger.info(f'{ticker} finalizado!')
            print(f'{ticker} finalizado!')   
        else:
            logger.error(f"Sem Preco Corrigido: {ticker}")
            print(f"Sem Preco Corrigido: {ticker}")
    return df_preco