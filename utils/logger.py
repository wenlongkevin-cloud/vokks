# utils/logger.py
# Marlong — 统一日志配置

import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("[%(levelname)s] %(name)s — %(message)s")
        )
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
