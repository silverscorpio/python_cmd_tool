""" Sets the Logger """

import logging
import os


def def_logger(log_dir: str):
    # log file definition
    logfile_name = "log_info.log"
    logfile_path = os.path.join(log_dir, "logs", logfile_name)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # handlers
    # file handler
    fh = logging.FileHandler(logfile_path)
    fh.setLevel(logging.DEBUG)

    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(message)s - %(module)s - %(funcName)s - %(lineno)d"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
