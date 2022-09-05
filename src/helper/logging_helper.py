from src.singleton.log_singleton import LogSingleton


def info(message: str):
    LogSingleton.get_logger().info(message)
    print(message, flush=True)


def warn(message: str):
    LogSingleton.get_logger().warn(message)


def error(message: str):
    LogSingleton.get_logger().error(message)
