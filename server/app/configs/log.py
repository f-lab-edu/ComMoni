import logging


def init_log():
    """
    log 초기화
    :return:
    """
    return logging.getLogger("root")


logger = init_log()
