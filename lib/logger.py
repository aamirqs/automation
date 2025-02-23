import logging
import inspect
import os
import datetime
from logging.handlers import RotatingFileHandler

LOG_LEVEL = 'ERROR'

DEBUG = 'DEBUG'
INFO = 'INFO'
CRITICAL = 'CRITICAL'


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = '%(asctime)s %(levelname)s %(message)s'

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomLogger:
    def __init__(self):
        self.logger = self.__setup_logger()

    def get_caller_info(self):
        frame = inspect.currentframe()
        frame = frame.f_back.f_back.f_back
        info = inspect.getframeinfo(frame)
        filename = os.path.basename(info.filename)
        return filename, info.lineno

    def get_log_level(self):
        level = LOG_LEVEL
        if level == 'DEBUG':
            return logging.DEBUG
        elif level == 'INFO':
            return logging.INFO
        elif level == 'CRITICAL':
            return logging.CRITICAL
        else:
            return logging.DEBUG

    def __setup_logger(self):
        log_level = self.get_log_level()
        logger = logging.getLogger()
        logger.setLevel(log_level)

        if "LOG_DIR" in os.environ:
            LOG_DIR = os.get_env('LOG_DIR')
            today_date = datetime.now().strftime("%Y-%m-%d")
            log_file = f"{LOG_DIR}/{today_date}.log"
            file_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=1)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(CustomFormatter())
            logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(CustomFormatter())
        logger.addHandler(stream_handler)
        return logger

    def log(self, level, message):  # todo pretty print dicts
        filename, line_no = self.get_caller_info()

        self.logger.log(level, f"{filename}:{line_no}: {message}")

    def debug(self, message):
        self.log(logging.DEBUG, message)

    def info(self, message):
        self.log(logging.INFO, message)

    def warning(self, message):
        self.log(logging.WARNING, message)

    def error(self, message):
        self.log(logging.ERROR, message)

    def critical(self, message):
        self.log(logging.CRITICAL, message)

    def set_log_level(self, log_level):
        if log_level == DEBUG:
            self.logger.setLevel(logging.DEBUG)
        elif log_level == INFO:
            self.logger.setLevel(logging.INFO)
        elif log_level == CRITICAL:
            self.logger.setLevel(logging.CRITICAL)


log = CustomLogger()
