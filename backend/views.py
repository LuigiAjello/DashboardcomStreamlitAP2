import pandas as pd
from datetime import date
import streamlit as st
from backend.apis import pegar_planilhao, get_preco_corrigido, get_preco_diversos
import plotly.graph_objects as go
from log_config.logging_config import logger  # Importando o logger centralizado

def filtrar_duplicado(df: pd.DataFrame, meio: str = None) -> pd.DataFrame:
    """
    Filtra empresas duplicadas no DataFrame, mantendo o ticker com maior valor na coluna especificada.

    Args:
        df (pd.DataFrame): DataFrame contendo as informações das empresas e seus tickers.
        meio (str, opcional): Coluna usada como critério para filtrar duplicatas. Padrão: 'volume'.

    Returns:
        pd.DataFrame: DataFrame sem empresas duplicadas.
    """
    logger.info("Iniciando filtragem de duplicados.")
    meio = meio or 'volume'
    try:
        df_dup = df[df.empresa.duplicated(keep=False)]
        lst_dup = df_dup.empresa.unique()
        lst_final = []
        for tic in lst_dup:
            tic_dup = df_dup[df_dup.empresa == tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]
            lst_final.append(tic_dup)
        lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values
        logger.info(f"Filtragem concluída com sucesso. Empresas duplicadas filtradas: {len(lst_final)}")
        return df[~df.ticker.isin(lst_dup)]
    except Exception as e:
        logger.error(f"Erro ao filtrar duplicados: {e}")
        raise


def pegar_df_planilhao(data_base: date) -> pd.DataFrame:
    """
    Obtém e processa o planilhão para uma data base específica, removendo duplicatas.

    Args:
        data_base (date): Data base para consulta do planilhão.

    Returns:
        pd.DataFrame: DataFrame com os dados processados e filtrados.
    """
    logger.info(f"Consultando planilhão para a data base: {data_base}")
    try:
        dados = pegar_planilhao(data_base)
        if dados:
            dados = dados['dados']
            planilhao = pd.DataFrame(dados)
            planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]
            df = filtrar_duplicado(planilhao)
            logger.info(f"Planilhão processado com sucesso. Total de linhas: {len(df)}")
            return df
        else:
            logger.warning("Nenhum dado retornado para o planilhão.")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erro ao processar o planilhão: {e}")
        raise


def carteira(data, indicador_rent, indicador_desc, num):
    """
    Gera uma carteira com base em indicadores de rentabilidade e desconto.

    Args:
        data (date): Data base para consulta do planilhão.
        indicador_rent (str): Indicador de rentabilidade para ranqueamento.
        indicador_desc (str): Indicador de desconto para ranqueamento.
        num (int): Número de ações a serem selecionadas.

    Returns:
        Tuple[pd.DataFrame, List[str]]: DataFrame com as ações selecionadas e lista de tickers.
    """
    logger.info(f"Gerando carteira com base nos indicadores: {indicador_rent}, {indicador_desc} e num ações: {num}")
    try:
        df = pegar_df_planilhao(data)
        if df.empty:
            logger.warning("Nenhum dado encontrado no planilhão para a data selecionada.")
            raise ValueError("Planilhão vazio.")

        colunas = ["ticker", "setor", "data_base", "roc", "roe", "roic", "earning_yield", "dividend_yield", "p_vp"]
        df = df[colunas]
        df = df.nlargest(300, indicador_rent).reset_index(drop=True)
        df['index_rent'] = df.index

        if indicador_desc == 'p_vp':
            df = df.nsmallest(300, indicador_desc).reset_index(drop=True)
        else:
            df = df.nlargest(300, indicador_desc).reset_index(drop=True)
        df['index_desc'] = df.index

        df["media"] = df["index_desc"] + df["index_rent"]
        df_sorted = df.sort_values(by=['media'], ascending=True).nsmallest(num, 'media').reset_index(drop=True)
        df_sorted.index = df_sorted.index + 1

        acoes_carteira = df_sorted['ticker'].tolist()
        logger.info(f"Carteira gerada com sucesso. Ações selecionadas: {acoes_carteira}")
        return df_sorted, acoes_carteira
    except Exception as e:
        logger.error(f"Erro ao gerar a carteira: {e}")
        raise


def pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira) -> pd.DataFrame:
    """
    Obtém os preços corrigidos das ações selecionadas em um intervalo de datas.

    Args:
        data_ini (date): Data inicial para consulta.
        data_fim (date): Data final para consulta.
        acoes_carteira (list): Lista de tickers das ações na carteira.

    Returns:
        pd.DataFrame: DataFrame com os preços corrigidos e retornos diários.
    """
    logger.info(f"Obtendo preços corrigidos de {data_ini} a {data_fim} para as ações: {acoes_carteira}")
    df_preco = pd.DataFrame()
    try:
        for ticker in acoes_carteira:
            dados = get_preco_corrigido(ticker, data_ini, data_fim)
            if dados and 'dados' in dados:
                df_temp = pd.DataFrame.from_dict(dados['dados'])
                df_temp['ticker'] = ticker
                df_temp['retorno_diario'] = df_temp['fechamento'].pct_change()
                df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
        if df_preco.empty:
            logger.warning("Nenhum dado retornado para os preços corrigidos.")
        else:
            logger.info(f"Preços corrigidos obtidos com sucesso. Total de linhas: {len(df_preco)}")
        return df_preco
    except Exception as e:
        logger.error(f"Erro ao obter preços corrigidos: {e}")
        raise


def pegar_df_preco_diversos(data_ini: date, data_fim: date) -> pd.DataFrame:
    """
    Obtém os preços do índice Ibovespa em um intervalo de datas.

    Args:
        data_ini (date): Data inicial para consulta.
        data_fim (date): Data final para consulta.

    Returns:
        pd.DataFrame: DataFrame com os preços do Ibovespa.
    """
    logger.info(f"Obtendo preços diversos de {data_ini} a {data_fim} para o Ibovespa.")
    try:
        df_preco = pd.DataFrame()
        dados = get_preco_diversos(data_ini, data_fim, 'ibov')
        if dados:
            dados = dados['dados']
            df_temp = pd.DataFrame.from_dict(dados)
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)
        if df_preco.empty:
            logger.warning("Nenhum dado retornado para os preços diversos.")
        else:
            logger.info(f"Preços diversos obtidos com sucesso. Total de linhas: {len(df_preco)}")
        return df_preco
    except Exception as e:
        logger.error(f"Erro ao obter preços diversos: {e}")
        raise


def plot_retorno_acumulado_carteira(df_carteira):
    """
    Plota o gráfico do retorno acumulado da carteira ao longo do tempo.

    Args:
        df_carteira (pd.DataFrame): DataFrame contendo os retornos diários da carteira.

    Returns:
        None: O gráfico é exibido na interface Streamlit.
    """

    logger.info("Plotando o retorno acumulado da carteira.")
    try:
        fig = go.Figure()
        df_carteira_grouped = df_carteira.groupby('data')['retorno_diario'].mean().reset_index()
        df_carteira_grouped['retorno_acumulado'] = (1 + df_carteira_grouped['retorno_diario']).cumprod() - 1

        fig.add_trace(go.Scatter(
            x=df_carteira_grouped['data'],
            y=df_carteira_grouped['retorno_acumulado'],
            mode='lines',
            name="Retorno Acumulado da Carteira",
            line=dict(color='blue', width=2)
        ))

        fig.update_layout(
            title="Retorno Acumulado da Carteira Total",
            xaxis_title="Data",
            yaxis_title="Retorno Acumulado",
            legend_title="Carteira",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        logger.info("Gráfico de retorno acumulado da carteira plotado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao plotar o retorno acumulado da carteira: {e}")
        raise


def plot_retorno_acumulado_ibov(df_ibov):
    """
    Plota o gráfico do retorno acumulado do Ibovespa ao longo do tempo.

    Args:
        df_ibov (pd.DataFrame): DataFrame contendo os preços e retornos diários do Ibovespa.

    Returns:
        None: O gráfico é exibido na interface Streamlit.
    """
    try:
        fig = go.Figure()
        df_ibov['retorno_diario'] = df_ibov['fechamento'].pct_change()
        df_ibov['retorno_acumulado'] = (1 + df_ibov['retorno_diario']).cumprod() - 1

        fig.add_trace(go.Scatter(
            x=df_ibov['data'],
            y=df_ibov['retorno_acumulado'],
            mode='lines',
            name="Retorno Acumulado do Ibovespa",
            line=dict(color='green', width=2)
        ))

        fig.update_layout(
            title="Retorno Acumulado do Ibovespa",
            xaxis_title="Data",
            yaxis_title="Retorno Acumulado",
            legend_title="Ibovespa",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        logger.info("Gráfico de retorno acumulado do Ibovespa plotado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao plotar o retorno acumulado do Ibovespa: {e}")
        raise


def plot_comparativo_acumulado(df_carteira: pd.DataFrame, df_ibov: pd.DataFrame):
    """
    Plota um gráfico comparativo do retorno acumulado da carteira e do Ibovespa ao longo do tempo.

    Args:
        df_carteira (pd.DataFrame): DataFrame com os retornos diários da carteira.
        df_ibov (pd.DataFrame): DataFrame com os preços e retornos diários do Ibovespa.

    Returns:
        None: O gráfico é exibido na interface Streamlit.
    """
    try:
        fig = go.Figure()
        df_carteira_grouped = df_carteira.groupby('data')['retorno_diario'].mean().reset_index()
        df_carteira_grouped['retorno_acumulado'] = (1 + df_carteira_grouped['retorno_diario']).cumprod() - 1

        df_ibov['retorno_diario'] = df_ibov['fechamento'].pct_change()
        df_ibov['retorno_acumulado'] = (1 + df_ibov['retorno_diario']).cumprod() - 1

        fig.add_trace(go.Scatter(
            x=df_carteira_grouped['data'],
            y=df_carteira_grouped['retorno_acumulado'],
            mode='lines',
            name="Retorno Acumulado da Carteira",
            line=dict(color='blue', width=2)
        ))

        fig.add_trace(go.Scatter(
            x=df_ibov['data'],
            y=df_ibov['retorno_acumulado'],
            mode='lines',
            name="Retorno Acumulado do Ibovespa",
            line=dict(color='green', width=2)
        ))

        fig.update_layout(
            title="Comparativo: Retorno Acumulado Carteira x Ibovespa",
            xaxis_title="Data",
            yaxis_title="Retorno Acumulado",
            legend_title="Comparação",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)
        logger.info("Gráfico comparativo acumulado plotado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao plotar gráfico comparativo acumulado: {e}")
        raise


def validar_data(data):
    """
    Valida a data fornecida, verificando se é válida para operações.

    Args:
        data (date): Data a ser validada.

    Raises:
        ValueError: Se a data for inválida por ser o dia atual, um final de semana ou uma data futura.
    """
    logger.info(f"Validando a data: {data}")
    try:
        if data == pd.to_datetime('today').date():
            raise ValueError("A data não pode ser o dia de hoje.")
        elif data.weekday() in [5, 6]:
            raise ValueError("Sábados e domingos não são permitidos.")
        elif data > pd.to_datetime('today').date():
            raise ValueError("Datas futuras não são permitidas.")
        logger.info("Data validada com sucesso.")
    except ValueError as e:
        logger.error(f"Data inválida: {e}")
        st.error(str(e))