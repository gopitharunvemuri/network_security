import logging
from datetime import datetime
import os

LOG_FILE = datetime.now().strftime("%d/%m/%Y")+"log_file"
log_file_path = os.path.join(os.getcwd(),"logs", LOG_FILE)

os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)