from backend.views import (
    pegar_df_planilhao,
    carteira,
    pegar_df_preco_corrigido,
    pegar_df_preco_diversos,
    plot_comparativo_acumulado
)
from log_config.logging_config import logger  # Importa o logger centralizado

def menu_planilhao(data_base):
    """
    Consulta os dados do Planilhão para uma data base específica e retorna um DataFrame.

    Args:
        data_base (str): Data base para a consulta ao planilhão no formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: DataFrame com os dados do Planilhão.

    Raises:
        ValueError: Se nenhum dado for encontrado ou ocorrer um erro na consulta.
    """
    logger.info(f"Iniciando consulta ao planilhão para a data base: {data_base}")
    try:
        df = pegar_df_planilhao(data_base)
        if df is None or df.empty:
            logger.warning(f"Nenhum dado retornado para a data base: {data_base}")
            raise ValueError("Nenhum dado foi encontrado para o Planilhão.")
        logger.info(f"Consulta ao planilhão bem-sucedida para a data base: {data_base} | Linhas retornadas: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Erro ao consultar o planilhão para a data base: {data_base} | {e}")
        raise


def menu_estrategia(data, indicador_rent, indicador_desc, num):
    """
    Calcula a estratégia com base nos indicadores fornecidos e retorna um DataFrame com os resultados.

    Args:
        data (pd.DataFrame): Dados utilizados para calcular a estratégia.
        indicador_rent (str): Indicador de rentabilidade utilizado.
        indicador_desc (str): Indicador de desconto utilizado.
        num (int): Número de ações a serem selecionadas na estratégia.

    Returns:
        pd.DataFrame: DataFrame com a estratégia gerada.

    Raises:
        ValueError: Se nenhum dado for retornado ou ocorrer um erro no cálculo.
    """
    logger.info(f"Calculando estratégia com indicador_rent: {indicador_rent}, indicador_desc: {indicador_desc}, num: {num}")
    try:
        df = carteira(data, indicador_rent, indicador_desc, num)
        if df is None or df.empty:
            logger.warning("Nenhum dado retornado pela função carteira.")
            raise ValueError("Nenhum dado foi encontrado para a estratégia.")
        logger.info(f"Estratégia gerada com sucesso | Linhas retornadas: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Erro ao calcular estratégia | Indicadores: {indicador_rent}, {indicador_desc}, Num: {num} | {e}")
        raise


def menu_graficos(data_ini, data_fim, acoes_carteira):
    """
    Gera os dados necessários para gráficos da carteira no período especificado.

    Args:
        data_ini (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.
        acoes_carteira (list): Lista de ações presentes na carteira.

    Returns:
        pd.DataFrame: DataFrame com os dados para os gráficos da carteira.

    Raises:
        ValueError: Se a carteira estiver vazia ou nenhum dado for encontrado.
    """
    logger.info(f"Iniciando geração de gráficos para a carteira | Data inicial: {data_ini}, Data final: {data_fim}, Ações: {acoes_carteira}")
    try:
        if not acoes_carteira:
            logger.error("Nenhuma ação na carteira foi fornecida para gerar gráficos.")
            raise ValueError("A carteira está vazia. Por favor, gere uma carteira antes de visualizar os gráficos.")

        df = pegar_df_preco_corrigido(data_ini, data_fim, acoes_carteira)
        if df is None or df.empty:
            logger.warning("Nenhum dado retornado para os gráficos da carteira.")
            raise ValueError("Nenhum dado foi encontrado para os gráficos da carteira.")
        logger.info(f"Gráficos gerados com sucesso para a carteira | Linhas retornadas: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Erro ao gerar gráficos para a carteira | {e}")
        raise


def grafico_ibov(data_ini, data_fim):
    """
    Gera os dados necessários para gráficos do Ibovespa no período especificado.

    Args:
        data_ini (str): Data inicial no formato 'YYYY-MM-DD'.
        data_fim (str): Data final no formato 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: DataFrame com os dados para os gráficos do Ibovespa.

    Raises:
        ValueError: Se nenhum dado for encontrado para o Ibovespa.
    """
    logger.info(f"Iniciando geração de gráficos para o Ibovespa | Data inicial: {data_ini}, Data final: {data_fim}")
    try:
        df = pegar_df_preco_diversos(data_ini, data_fim)
        if df is None or df.empty:
            logger.warning("Nenhum dado retornado para os gráficos do Ibovespa.")
            raise ValueError("Nenhum dado foi encontrado para os gráficos do Ibovespa.")
        logger.info(f"Gráficos do Ibovespa gerados com sucesso | Linhas retornadas: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Erro ao gerar gráficos para o Ibovespa | {e}")
        raise


def Comparacao_graficos(df_carteira, df_ibov):
    """
    Gera um gráfico comparativo entre a carteira de ações e o Ibovespa.

    Args:
        df_carteira (pd.DataFrame): Dados da carteira de ações.
        df_ibov (pd.DataFrame): Dados do Ibovespa.

    Raises:
        ValueError: Se os dados da carteira ou do Ibovespa estiverem ausentes ou inválidos.
    """
    logger.info("Iniciando comparação de gráficos.")
    try:
        if df_carteira is None or df_carteira.empty:
            logger.error("O DataFrame da carteira está vazio ou é inválido.")
            raise ValueError("Dados da carteira não estão disponíveis para a comparação.")
        if df_ibov is None or df_ibov.empty:
            logger.error("O DataFrame do Ibovespa está vazio ou é inválido.")
            raise ValueError("Dados do Ibovespa não estão disponíveis para a comparação.")

        # Gera o gráfico comparativo usando a função plot_comparativo_acumulado
        plot_comparativo_acumulado(df_carteira, df_ibov)
        logger.info(f"Comparação de gráficos gerada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao gerar comparação de gráficos | {e}")
        raise
