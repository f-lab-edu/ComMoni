from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PREFIX_ENDPOINT: str = "/api"

    # Database
    USERNAME: str = "kristoff"
    PASSWORD: str = "1234"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "commonidb"
    SQLALCHEMY_DATABASE_URI: str = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # JWT / Auth
    SECRET_KEY: str = "0548a115e749bd446115d6c05e95838b2f7b47568e110186e0fe81fca376e19d"
    ALGORITHM: str = "HS256"
    TOKEN_URL: str = "/api/v1/auth/login"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20  # minute
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 15  # date
    DATE_BEFORE_EXPIRATION: int = 2  # date

    # Redis
    REDIS_IP: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB_NUM: int = 0

    class Config:
        env_file = '.env'


settings = Settings()
