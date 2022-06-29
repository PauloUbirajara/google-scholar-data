from logging import basicConfig, getLogger, INFO
from os import makedirs
from os.path import join, exists

from src.helper.date_helper import timestamp_as_string


class LogSingleton:
    @staticmethod
    def get():
        if not hasattr(LogSingleton, '__logger'):
            setattr(LogSingleton, '__logger', new_logger())

        return getattr(LogSingleton, '__logger')


def new_logger():
    log_folder = '.logs'
    if not exists(log_folder):
        makedirs(log_folder)

    log_name = f'app_{timestamp_as_string()}.log'
    log_path = join(log_folder, log_name)

    LOG_FORMAT = '(%(asctime)s) %(levelname)s: %(message)s'

    basicConfig(
        filename=log_path,
        format=LOG_FORMAT,
        level=INFO,
        encoding='utf-8'
    )
    return getLogger()
