import logging, logging.config


def init_log():
    """
    log 초기화
    :return:
    """
    logging.config.fileConfig("log.ini")
    return logging.getLogger("root")


logger = init_log()
