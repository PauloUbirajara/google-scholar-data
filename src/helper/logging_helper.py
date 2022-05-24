from src.singleton.log_singleton import LogSingleton

__log = LogSingleton.get()


def info(message: str):
    __log.info(message)


def warn(message: str):
    __log.warn(message)


def error(message: str):
    __log.error(message)
