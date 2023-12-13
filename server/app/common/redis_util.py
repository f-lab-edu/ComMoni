from typing import Generator

import redis

from app.configs.config import settings


def get_redis() -> Generator:
    """
    FastAPI Depends에서 사용할 Redis connection
    :return: Generator
    """
    try:
        connection = redis.StrictRedis(
            host=settings.REDIS_IP,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB_NUM)
        yield connection
    finally:
        connection.close()
