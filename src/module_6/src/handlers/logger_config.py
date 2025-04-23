import logging
from logging.handlers import RotatingFileHandler


logger_status = logging.getLogger("status_logger")
logger_status.setLevel(logging.INFO)

logger_predict = logging.getLogger("predict_logger")
logger_predict.setLevel(logging.INFO)

logger_metrics = logging.getLogger("metrics_logger")
logger_metrics.setLevel(logging.INFO)

# formate
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# create file
file_handler = RotatingFileHandler(
    "src/module_6/logs/api.log", maxBytes=1000000, backupCount=5
)
file_handler.setFormatter(formatter)

# define a file to each logger
logger_status.addHandler(file_handler)
logger_predict.addHandler(file_handler)
logger_metrics.addHandler(file_handler)
