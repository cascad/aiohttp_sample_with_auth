from logging.handlers import RotatingFileHandler
import logging
import os

from settings import PROJECT_PREFIX


def config_logger():
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    logger = logging.getLogger(PROJECT_PREFIX)
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler("logs/main.log", maxBytes=10 * 1024 * 1024, backupCount=10, encoding="utf8")
    handler.setLevel(logging.WARN)
    logger.addHandler(handler)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger
