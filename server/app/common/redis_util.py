from typing import Generator

from redis import StrictRedis
from redis.exceptions import RedisError

from app.configs.config import settings


class RedisUtilError(Exception):
    pass


def get_redis() -> Generator:
    """
    FastAPI Depends에서 사용할 Redis connection
    :return: Generator
    """
    connection = RedisUtil()
    try:
        yield connection
    finally:
        connection.close()


class RedisUtil:
    def __init__(self):
        """Redis연결 생성"""
        self.connection = StrictRedis(
            host=settings.REDIS_IP,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB_NUM,
            charset="utf-8",
            decode_responses=True)

    def close(self):
        """Redis 연결 해제"""
        self.connection.close()

    def get(self, key: str):
        """Redis에서 값 가져오기"""
        try:
            return self.connection.get(key)
        except RedisError as err:
            raise RedisUtilError(err)

    def set(self, key: str, value: str):
        """Redis에 값 저장"""
        try:
            self.connection.set(key, value)
        except RedisError as err:
            raise RedisUtilError(err)

    def delete(self, key: str):
        """Redis에 키 삭제"""
        try:
            self.connection.delete(key)
        except RedisError as err:
            raise RedisUtilError(err)

    def set_with_expire(self, key: str, value: str, expire_minutes: int):
        """Redis에 값 저장(만료시간 추가)"""
        try:
            self.connection.setex(name=key, value=value, time=expire_minutes)
        except RedisError as err:
            raise RedisUtilError(err)
