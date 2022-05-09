from src.singleton.log_singleton import log_singleton


def info(message: str):
    log_singleton.get().info(message)


def warn(message: str):
    log_singleton.get().warn(message)


def error(message: str):
    log_singleton.get().error(message)
