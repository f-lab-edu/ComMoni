from typing import Optional

from pydantic import BaseModel


class ComManageBase(BaseModel):
    """
    Attributes
        - host_id : 호스트 아이디
        - user_id : 사용자 아이디
        - host_name : 호스트 이름
        - host_ip : 호스트 아이피
        - memory : 메모리 용량
        - disk : 디스크 용량
    """
    user_id: Optional[str] = None
    host_id: Optional[int] = None
    host_name: Optional[str] = None
    host_ip: Optional[str] = None
    memory: Optional[str] = None
    disk: Optional[str] = None
    deleted: Optional[bool] = None

    class Config:
        from_attributes = True


class ComManage(ComManageBase):
    pass


class ComManageByUser(ComManageBase):
    user_id: str


class ComManageByHost(ComManageBase):
    host_id: int


class ComManageResponse(BaseModel):
    host_id: int
