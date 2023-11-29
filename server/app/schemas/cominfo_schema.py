from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ComInfoBase(BaseModel):
    """
        모니터링 데이터

        Attributes
            - host_id : 호스트 아이디
            - cpu_utilization : cpu 사용률
            - memory_utilization : 메모리 사용률
            - disk__utilization : 디스크 사용률
            - make_datetime : 데이터 생성 날짜/시간
    """
    host_id: Optional[int] = None
    cpu_utilization: Optional[float] = None
    memory_utilization: Optional[float] = None
    disk_utilization: Optional[float] = None
    make_datetime: Optional[datetime] = None

    class Config:
        from_attributes = True


class ComInfo(ComInfoBase):
    pass


class ComInfoGet(ComInfoBase):
    host_id: int


class ComInfoCreate(ComInfoBase):
    host_id: int
    cpu_utilization: float
    memory_utilization: float
    disk_utilization: float
    make_datetime: datetime


class ComInfoRTBase(BaseModel):
    """
        모니터링 데이터

        Attributes
            - host_id : 호스트 아이디
            - cpu_utilization : cpu 사용률
            - memory_utilization : 메모리 사용률
            - disk__utilization : 디스크 사용률
            - make_datetime : 데이터 생성 날짜/시간
    """
    host_id: Optional[int] = None
    cpu_utilization: Optional[float] = None
    memory_utilization: Optional[float] = None
    disk_utilization: Optional[float] = None
    make_datetime: Optional[datetime] = None
    update_datetime: Optional[datetime] = None

    class Config:
        from_attributes = True


class ComInfoRT(ComInfoRTBase):
    host_id: int
