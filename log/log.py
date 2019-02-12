import logging
import config.config as conf


class Logger:

    def __init__(self):
        cfg = conf.config_parser()
        fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
        logging.basicConfig(format=fmt, filename=cfg.get("log", "log.file.path"), level=logging.INFO)

    def get_logger(self):
        return logging
