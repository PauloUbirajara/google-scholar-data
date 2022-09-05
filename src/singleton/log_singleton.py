from logging import FileHandler, Formatter, getLogger, INFO, Logger
from os import makedirs
from os.path import join

from src.helper.date_helper import timestamp_as_string


def new_logger_handler():
    log_folder = '.logs'

    makedirs(log_folder, exist_ok=True)

    log_name = f'app_{timestamp_as_string()}.log'
    log_path = join(log_folder, log_name)
    handler = FileHandler(filename=log_path, mode='w', encoding='utf-8')

    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    handler.setFormatter(Formatter(LOG_FORMAT))
    return handler


def new_logger():
    root_logger = getLogger(__name__)
    root_logger.setLevel(INFO)

    root_logger.addHandler(new_logger_handler())

    return root_logger


class LogSingleton:
    logger: Logger

    @staticmethod
    def get_logger():
        if not LogSingleton.logger:
            LogSingleton.logger = new_logger()

        return LogSingleton.logger
