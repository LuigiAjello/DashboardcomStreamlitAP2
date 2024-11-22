import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent.resolve()

# Diretórios do backend e frontend
BACK_DIR = str(BASE_DIR / "backend")
FRONT_DIR = str(BASE_DIR / "frontend")

# Diretório para os logs
LOG_DIR = str(BASE_DIR / "logs")

# Criação da pasta de logs (caso não exista)
os.makedirs(LOG_DIR, exist_ok=True)

# Configuração do logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=f"{LOG_DIR}/app.log",
    filemode="a"
)
