from logging import FileHandler, Formatter, getLogger, INFO
from os import makedirs
from os.path import join

from src.helper.date_helper import timestamp_as_string


def new_logger_formatter():
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = Formatter(LOG_FORMAT)
    return formatter


def new_logger_handler(log_name: str):
    log_folder = '.logs'

    makedirs(log_folder, exist_ok=True)

    log_path = join(log_folder, log_name)
    handler = FileHandler(filename=log_path, mode='w', encoding='utf-8')

    handler.setFormatter(new_logger_formatter())
    return handler

    # TODO Mudar encoding, mas criar dois arquivos ou criar um e ter encoding errado
    # log_name = f'app_{timestamp_as_string()}.log'
    #
    # log_folder = '.logs'
    #
    # makedirs(log_folder, exist_ok=True)
    #
    # log_path = join(log_folder, log_name)
    # basicConfig(filename=log_path, encoding='utf8', level=INFO)


def setup_logging():
    root_logger = getLogger()

    if root_logger.level != INFO:
        root_logger.setLevel(INFO)

    if not root_logger.handlers:
        log_name = f'app_{timestamp_as_string()}.log'
        root_logger.addHandler(new_logger_handler(log_name))


def info(message: str):
    getLogger().info(message)
    print(message, flush=True)


def warn(message: str):
    getLogger().warning(message)


def error(message: str):
    getLogger().error(message)
