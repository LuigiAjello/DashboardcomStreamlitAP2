import pandas as pd
from datetime import date
import streamlit as st
from backend.apis import pegar_planilhao, get_preco_corrigido, get_preco_diversos
import plotly.graph_objects as go
from log_config.logging_config import logger  # Importando o logger centralizado para logs consistentes.

# Filtrar empresas duplicadas
def filtrar_duplicado(df: pd.DataFrame, meio: str = None) -> pd.DataFrame:
    """
    Filtra empresas duplicadas no DataFrame, mantendo o ticker com maior valor na coluna especificada.

    Args:
        df (pd.DataFrame): DataFrame contendo as informações das empresas e seus tickers.
        meio (str, opcional): Coluna usada como critério para filtrar duplicatas. Padrão: 'volume'.

    Returns:
        pd.DataFrame: DataFrame sem empresas duplicadas.
    """
    logger.info("Iniciando filtragem de duplicados.")  # Log inicial do processo.
    meio = meio or 'volume'  # Define a coluna padrão como 'volume' caso não seja especificado.
    try:
        # Identificar empresas duplicadas
        df_dup = df[df.empresa.duplicated(keep=False)]  # Filtra linhas onde a coluna 'empresa' está duplicada.
        lst_dup = df_dup.empresa.unique()  # Obtém os nomes únicos das empresas duplicadas.
        lst_final = []

        # Seleciona o ticker com maior valor na coluna especificada para cada empresa duplicada.
        for tic in lst_dup:
            tic_dup = df_dup[df_dup.empresa == tic].sort_values(by=[meio], ascending=False)['ticker'].values[0]
            lst_final.append(tic_dup)

        # Remove duplicatas restantes com base nos tickers selecionados.
        lst_dup = df_dup[~df_dup.ticker.isin(lst_final)]['ticker'].values
        logger.info(f"Filtragem concluída com sucesso. Empresas duplicadas filtradas: {len(lst_final)}")
        return df[~df.ticker.isin(lst_dup)]  # Retorna o DataFrame sem duplicatas.
    except Exception as e:
        logger.error(f"Erro ao filtrar duplicados: {e}")  # Log de erro detalhado.
        raise

# Processar e filtrar o planilhão
def pegar_df_planilhao(data_base: date) -> pd.DataFrame:
    """
    Obtém e processa o planilhão para uma data base específica, removendo duplicatas.

    Args:
        data_base (date): Data base para consulta do planilhão.

    Returns:
        pd.DataFrame: DataFrame com os dados processados e filtrados.
    """
    logger.info(f"Consultando planilhão para a data base: {data_base}")  # Log do início do processo.
    try:
        dados = pegar_planilhao(data_base)  # Obtém dados do planilhão para a data base fornecida.
        if dados:
            dados = dados['dados']  # Extrai os dados relevantes.
            planilhao = pd.DataFrame(dados)  # Converte para DataFrame.
            planilhao['empresa'] = [ticker[:4] for ticker in planilhao.ticker.values]  # Cria coluna 'empresa'.
            df = filtrar_duplicado(planilhao)  # Remove duplicatas usando a função `filtrar_duplicado`.
            logger.info(f"Planilhão processado com sucesso. Total de linhas: {len(df)}")
            return df
        else:
            logger.warning("Nenhum dado retornado para o planilhão.")
            return pd.DataFrame()  # Retorna um DataFrame vazio se não houver dados.
    except Exception as e:
        logger.error(f"Erro ao processar o planilhão: {e}")
        raise

# Gerar carteira baseada em indicadores
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
        # Obtém os dados do planilhão processado.
        df = pegar_df_planilhao(data)
        if df.empty:
            logger.warning("Nenhum dado encontrado no planilhão para a data selecionada.")
            raise ValueError("Planilhão vazio.")

        # Seleciona as colunas de interesse.
        colunas = ["ticker", "setor", "data_base", "roc", "roe", "roic", "earning_yield", "dividend_yield", "p_vp"]
        df = df[colunas]

        # Filtra as ações com base no indicador de rentabilidade.
        df = df.nlargest(300, indicador_rent).reset_index(drop=True)
        df['index_rent'] = df.index

        # Filtra as ações com base no indicador de desconto.
        if indicador_desc == 'p_vp':
            df = df.nsmallest(300, indicador_desc).reset_index(drop=True)
        else:
            df = df.nlargest(300, indicador_desc).reset_index(drop=True)
        df['index_desc'] = df.index

        # Calcula a média dos rankings e seleciona as melhores ações.
        df["media"] = df["index_desc"] + df["index_rent"]
        df_sorted = df.sort_values(by=['media'], ascending=True).nsmallest(num, 'media').reset_index(drop=True)
        df_sorted.index = df_sorted.index + 1

        # Extrai os tickers das ações selecionadas.
        acoes_carteira = df_sorted['ticker'].tolist()
        logger.info(f"Carteira gerada com sucesso. Ações selecionadas: {acoes_carteira}")
        return df_sorted, acoes_carteira
    except Exception as e:
        logger.error(f"Erro ao gerar a carteira: {e}")
        raise
# Obter preços corrigidos para os tickers da carteira
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
            # Chama a API para obter dados do ticker no intervalo fornecido.
            dados = get_preco_corrigido(ticker, data_ini, data_fim)
            if dados and 'dados' in dados:
                df_temp = pd.DataFrame.from_dict(dados['dados'])  # Converte os dados para DataFrame.
                df_temp['ticker'] = ticker  # Adiciona a coluna de ticker.
                df_temp['retorno_diario'] = df_temp['fechamento'].pct_change()  # Calcula o retorno diário.
                df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)  # Adiciona ao DataFrame final.
        if df_preco.empty:
            logger.warning("Nenhum dado retornado para os preços corrigidos.")
        else:
            logger.info(f"Preços corrigidos obtidos com sucesso. Total de linhas: {len(df_preco)}")
        return df_preco
    except Exception as e:
        logger.error(f"Erro ao obter preços corrigidos: {e}")
        raise

# Obter preços do índice Ibovespa
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
        dados = get_preco_diversos(data_ini, data_fim, 'ibov')  # Obtém dados do índice Ibovespa.
        if dados:
            dados = dados['dados']
            df_temp = pd.DataFrame.from_dict(dados)  # Converte para DataFrame.
            df_preco = pd.concat([df_preco, df_temp], axis=0, ignore_index=True)  # Adiciona ao DataFrame final.
        if df_preco.empty:
            logger.warning("Nenhum dado retornado para os preços diversos.")
        else:
            logger.info(f"Preços diversos obtidos com sucesso. Total de linhas: {len(df_preco)}")
        return df_preco
    except Exception as e:
        logger.error(f"Erro ao obter preços diversos: {e}")
        raise

# Plotar o retorno acumulado da carteira
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
        # Calcula o retorno acumulado agrupado por data.
        df_carteira_grouped = df_carteira.groupby('data')['retorno_diario'].mean().reset_index()
        df_carteira_grouped['retorno_acumulado'] = (1 + df_carteira_grouped['retorno_diario']).cumprod() - 1

        # Adiciona a linha de retorno acumulado da carteira ao gráfico.
        fig.add_trace(go.Scatter(
            x=df_carteira_grouped['data'],
            y=df_carteira_grouped['retorno_acumulado'],
            mode='lines',
            name="Retorno Acumulado da Carteira",
            line=dict(color='blue', width=2)
        ))

        # Configura o layout do gráfico.
        fig.update_layout(
            title="Retorno Acumulado da Carteira Total",
            xaxis_title="Data",
            yaxis_title="Retorno Acumulado",
            legend_title="Carteira",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)  # Exibe o gráfico no Streamlit.
        logger.info("Gráfico de retorno acumulado da carteira plotado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao plotar o retorno acumulado da carteira: {e}")
        raise

# Plotar o retorno acumulado do Ibovespa
def plot_retorno_acumulado_ibov(df_ibov):
    """
    Plota o gráfico do retorno acumulado do Ibovespa ao longo do tempo.

    Args:
        df_ibov (pd.DataFrame): DataFrame contendo os preços e retornos diários do Ibovespa.

    Returns:
        None: O gráfico é exibido na interface Streamlit.
    """
    logger.info("Plotando o retorno acumulado do Ibovespa.")
    try:
        fig = go.Figure()
        # Calcula o retorno diário e acumulado do Ibovespa.
        df_ibov['retorno_diario'] = df_ibov['fechamento'].pct_change()
        df_ibov['retorno_acumulado'] = (1 + df_ibov['retorno_diario']).cumprod() - 1

        # Adiciona a linha de retorno acumulado do Ibovespa ao gráfico.
        fig.add_trace(go.Scatter(
            x=df_ibov['data'],
            y=df_ibov['retorno_acumulado'],
            mode='lines',
            name="Retorno Acumulado do Ibovespa",
            line=dict(color='green', width=2)
        ))

        # Configura o layout do gráfico.
        fig.update_layout(
            title="Retorno Acumulado do Ibovespa",
            xaxis_title="Data",
            yaxis_title="Retorno Acumulado",
            legend_title="Ibovespa",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)  # Exibe o gráfico no Streamlit.
        logger.info("Gráfico de retorno acumulado do Ibovespa plotado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao plotar o retorno acumulado do Ibovespa: {e}")
        raise

# Plotar comparativo entre carteira e Ibovespa
def plot_comparativo_acumulado(df_carteira: pd.DataFrame, df_ibov: pd.DataFrame):
    """
    Plota um gráfico comparativo do retorno acumulado da carteira e do Ibovespa ao longo do tempo.

    Args:
        df_carteira (pd.DataFrame): DataFrame com os retornos diários da carteira.
        df_ibov (pd.DataFrame): DataFrame com os preços e retornos diários do Ibovespa.

    Returns:
        None: O gráfico é exibido na interface Streamlit.
    """
    logger.info("Plotando gráfico comparativo acumulado.")
    try:
        fig = go.Figure()

        # Calcula o retorno acumulado da carteira.
        df_carteira_grouped = df_carteira.groupby('data')['retorno_diario'].mean().reset_index()
        df_carteira_grouped['retorno_acumulado'] = (1 + df_carteira_grouped['retorno_diario']).cumprod() - 1

        # Calcula o retorno acumulado do Ibovespa.
        df_ibov['retorno_diario'] = df_ibov['fechamento'].pct_change()
        df_ibov['retorno_acumulado'] = (1 + df_ibov['retorno_diario']).cumprod() - 1

        # Adiciona ambas as séries de retorno ao gráfico.
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

        # Configura o layout do gráfico.
        fig.update_layout(
            title="Comparativo: Retorno Acumulado Carteira x Ibovespa",
            xaxis_title="Data",
            yaxis_title="Retorno Acumulado",
            legend_title="Comparação",
            hovermode="x unified",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)  # Exibe o gráfico no Streamlit.
        logger.info("Gráfico comparativo acumulado plotado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao plotar gráfico comparativo acumulado: {e}")
        raise

# Validar data fornecida pelo usuário
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
        # Verifica se a data é o dia atual.
        if data == pd.to_datetime('today').date():
            raise ValueError("A data não pode ser o dia de hoje.")
        # Verifica se a data é um sábado ou domingo.
        elif data.weekday() in [5, 6]:
            raise ValueError("Sábados e domingos não são permitidos.")
        # Verifica se a data é futura.
        elif data > pd.to_datetime('today').date():
            raise ValueError("Datas futuras não são permitidas.")
        logger.info("Data validada com sucesso.")
    except ValueError as e:
        logger.error(f"Data inválida: {e}")
        st.error(str(e))  # Exibe o erro na interface Streamlit.
