import logging
import sys

def setup_logging():
    # Handlers - Formats - Levels
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler("appdata")
    log_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Define LOGGER
    logger = logging.getLogger('APP')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger