import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
LOG_PATH = str(ROOT) + "/log_files/app.log"

def get_logger():
    logger = logging.getLogger("ai_web_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        # 日志分片
        file_handler = RotatingFileHandler(
            LOG_PATH, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        # 控制台日志
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

logger = get_logger()
