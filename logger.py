import logging
import sys
from logging.handlers import RotatingFileHandler

def get_logger(name,log_file):
    logger =logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(fmt='%(asctime)s | %(name)s | %(levelname)s | %(funcName)s | %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    rotating_handler = RotatingFileHandler(filename=log_file,maxBytes=1024 * 1024,backupCount=3)
    rotating_handler.setLevel(logging.DEBUG)
    rotating_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(rotating_handler)
    logger.propagate = False

    return logger
