from sqlalchemy import Column, Integer, DateTime, Float

from app.db.base import Base


class ComInfo(Base):
    """
        모니터링 데이터 모델

        Attributes
            - sequence : 데이터 순서
            - host_id : 호스트 아이디
            - cpu_utilization : cpu 사용률
            - memory_utilization : 메모리 사용률
            - disk__utilization : 디스크 사용률
            - make_datetime : 데이터 생성 날짜/시간
    """
    sequence = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer)
    cpu_utilization = Column(Float)
    memory_utilization = Column(Float)
    disk_utilization = Column(Float)
    make_datetime = Column(DateTime)


class ComInfoRT(Base):
    """
        실시간 모니터링 정보

        Attributes
            - host_id : 호스트 아이디
            - cpu_utilization : cpu 사용률
            - memory_utilization : 메모리 사용률
            - disk__utilization : 디스크 사용률
            - make_datetime : 데이터 생성 시간
    """
    host_id = Column(Integer, primary_key=True)
    cpu_utilization = Column(Float)
    memory_utilization = Column(Float)
    disk_utilization = Column(Float)
    make_datetime = Column(DateTime)
