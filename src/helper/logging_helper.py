from src.singleton.log_singleton import LogSingleton


def info(message: str):
    LogSingleton.get().info(message)


def warn(message: str):
    LogSingleton.get().warn(message)


def error(message: str):
    LogSingleton.get().error(message)
