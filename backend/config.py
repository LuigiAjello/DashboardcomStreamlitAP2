import os
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent.resolve()
BACK_DIR = str(BASE_DIR)+ "/backend"
FRONT_DIR = str(BACK_DIR) + "/frontend"
LOG_DIR = str(BACK_DIR) + "/frontend"
import logging 
logging.basicConfig(level=logging.INFO,
                    format = "%(asctime)s - %(name)s- %(levelname)s - %(message)s ",
                    filename= f"{LOG_DIR}/app.log",
                    filemode="a")