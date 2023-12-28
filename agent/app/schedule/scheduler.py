from typing import Any, List, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler:
    """
    AsyncIOScheduler를 이용한 스케줄러 클래스
    """

    def __init__(self):
        """
        생성자. 스케줄러 객체 생성 및 실행
        """
        self.__scheduler = AsyncIOScheduler()
        self.__scheduler.start()

    def shutdown(self) -> None:
        """
        스케줄러에 등록된 모든 job 정지
        :return:
        """
        if self.__scheduler.running:
            self.__scheduler.shutdown()
        else:
            print(f"scheduler is not running state")

    def add_cron_schedule(self, func: Any, second: str, args: List = None) -> None:
        """
        스케줄러에 job 추가 (cron 형태만 사용)
        :param func: 호춣될 함수
        :param second: 호출 주기
        :param args: 호출될 함수에 전달할 파라미터
        :return: None
        """
        self.__scheduler.add_job(func=func, trigger="cron", second=second, args=args, misfire_grace_time=None)
