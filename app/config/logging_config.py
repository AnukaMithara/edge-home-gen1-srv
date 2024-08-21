import logging
import sys

from app.config.config import LOG_LEVEL

FORMAT = '%(asctime)s  %(name)s:%(lineno)s -> (%(levelname)s)  %(message)s'

logging.getLogger("urllib3").setLevel(logging.DEBUG)


def get_logger(class_name):
    formatter = logging.Formatter(FORMAT)
    logger = logging.getLogger(class_name)
    logger.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = 0
    return logger
