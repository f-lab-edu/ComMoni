from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswdUtil:
    @classmethod
    def verify(cls, plain: str, hashed: str) -> bool:
        """
        비밀번호 해시값 비교 인증
        :param plain: 평문 비밀번호
        :param hashed: 해시된 비밀번호
        :return: bool
        """
        return pwd_context.verify(plain, hashed)

    @classmethod
    def get_hash(cls, password: str) -> str:
        """
        비밀번호 해시하여 반환
        :param password: 원본 비밀번호
        :return: 해시된 비밀번호
        """
        return pwd_context.hash(password)
