from datetime import datetime
from logging import basicConfig, getLogger, Logger
from os.path import dirname


class LogSingleton:
    __logger: Logger = None

    def get(self):
        if not LogSingleton.__logger:
            timestamp = datetime.now()
            formatted_timestamp = timestamp.strftime('%d_%m_%Y_%H_%M_%S')

            log_path = f'{dirname(__file__)}/../logs/app_{formatted_timestamp}.log'

            __FORMAT = '(%(asctime)s) %(levelname)s: %(message)s'
            basicConfig(filename=log_path, format=__FORMAT)
            LogSingleton.__logger = getLogger()

        return LogSingleton.__logger


log_singleton = LogSingleton()
