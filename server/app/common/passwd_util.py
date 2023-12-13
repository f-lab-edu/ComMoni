from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    비밀번호 해시값 비교 인증
    :param plain_password: 평문 비밀번호
    :param hashed_password: 해시된 비밀번호
    :return: bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    비밀번호 해시하여 반환
    :param password: 원본 비밀번호
    :return: 해시된 비밀번호
    """
    return pwd_context.hash(password)
