from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class ComManage(Base):
    """
        모니터링 대상인 호스트 정보

        Attributes:
            - host_id : 호스트 아이디
            - user_id : 사용자 아이디
            - host_name : 호스트 이름
            - host_ip : 호스트 아이피
            - memory : 메모리 용량
            - disk : 디스크 용량
    """
    host_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), primary_key=True)
    host_name = Column(String(50))
    host_ip = Column(String(20))
    memory = Column(String(20))
    disk = Column(String(20))
    deleted = Column(Boolean, default=False)
