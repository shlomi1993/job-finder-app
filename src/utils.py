import logging


def get_logger(logger_name: str) -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(logger_name)
    logger.parent.handlers.clear()
    formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger