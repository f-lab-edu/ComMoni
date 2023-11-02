from sqlalchemy import Column, Integer, String

from app.db.base import Base


class User(Base):
    """
        사용자 객체 모델

        Attributes
            - user_id : 사용자 아이디
            - user_pw : 사용자 비밀번호
            - user_name : 사용자 이름
    """
    user_id = Column(String(50), primary_key=True)
    user_pw = Column(String(32))
    user_name = Column(String(20))
