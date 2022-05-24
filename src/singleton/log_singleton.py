from logging import basicConfig, getLogger, Logger, INFO
from os import makedirs
from os.path import join, exists

from src.helper.date_helper import timestamp_as_string

LOG_FORMAT = '(%(asctime)s) %(levelname)s: %(message)s'


class LogSingleton:
    __logger: Logger = None

    @staticmethod
    def get():
        if LogSingleton.__logger is None:
            LogSingleton.__logger = LogSingleton.__new_logger()

        return LogSingleton.__logger

    @staticmethod
    def __new_logger():
        formatted_timestamp = timestamp_as_string()

        log_folder = '.logs'
        if not exists(log_folder):
            makedirs(log_folder)

        log_name = f'app_{formatted_timestamp}.log'
        log_path = join(log_folder, log_name)
        basicConfig(filename=log_path, format=LOG_FORMAT, level=INFO)
        return getLogger()
