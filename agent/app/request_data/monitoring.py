from datetime import datetime

import psutil
import orjson


class NormalData:
    """
    모니터링 데이터를 생성
    """

    def __init__(self, host_id: int):
        """
        등록된 호스트 아이디
        :param host_id: Host ID 값
        """
        self.host_id = host_id
        self.cpu_usage = psutil.cpu_percent(interval=1)
        self.memory_usage = psutil.virtual_memory().percent
        self.disk_usage = psutil.disk_usage('/').percent
        self.maketime = str(datetime.now())

    def make(self) -> bytes:
        """
        데이터를 json 형태로 반환
        :return:
        """
        return orjson.dumps({
            "host_id": self.host_id,
            "cpu_utilization": self.cpu_usage,
            "memory_utilization": self.memory_usage,
            "disk_utilization": self.disk_usage,
            "make_datetime": self.maketime
        })
