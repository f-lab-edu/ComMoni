import asyncio
from asyncio.events import AbstractEventLoop
from signal import SIGINT, SIGTERM

from app.configs.log import logger


def handler(sig):
    """
    signal 처리를 위한 handler 함수
    :param sig: 프로세스에서 받은 시그널
    :return: None
    """
    logger.info(f"[sig handelr] recv signal : {sig}")
    loop = asyncio.get_running_loop()

    for task in asyncio.all_tasks(loop=loop):
        task.cancel()

    logger.info(f"[sig handelr] all tasks canceled")

    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)


def set_signal(loop: AbstractEventLoop):
    """
    현재 동작중인 eventloop에 signal 처리 등록
    :param loop:
    :return:
    """
    for sig in [SIGTERM, SIGINT]:
        loop.add_signal_handler(sig, handler, sig)
