import logging


def get_logger(name):
    logger = logging.getLogger(name)
    level = logging.INFO
    logger.setLevel(level)
    formatter = logging.Formatter(
        (
        '{"unix_time": %(created)s, "time": "%(asctime)s", "module": "%(name)s",'
        ' "lineno": %(lineno)s, "level": "%(levelname)s", "msg": "%(message)s"}'
        )
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger

def clone_log_config(base_logger: logging.Logger, target_logger: logging.Logger):
    target_logger.handlers.clear()
    target_logger.addHandler(base_logger.handlers[0])
    target_logger.setLevel(base_logger.level)