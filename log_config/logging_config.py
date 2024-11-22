import logging
import os

# Diretório para armazenar os logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=f"{LOG_DIR}/app.log",
    filemode="a"
)

# Logger exportado
logger = logging.getLogger(__name__)
