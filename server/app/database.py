from typing import Generator, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.configs.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    id: Any
    __name__: str

    def __init__(self, **kwargs):
        """
            dict to object 변환용 생성자
            :param kwargs: 클래스로 변환할 딕셔너리
        """
        self.__dict__.update(kwargs)

    @declared_attr
    def __tablename__(cls) -> str:
        """
            __table_name__을 자동으로 생성
        """
        return cls.__name__.lower()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
