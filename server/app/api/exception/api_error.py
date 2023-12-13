from fastapi import status


class ApiErrorBase(Exception):
    """
    API Exception 처리를 위한 베이스 클래스
    Attributes:
        - status : http status code
        - message : 상세 내용
    """
    status: int
    message: str
    headers: dict = None

    def __init__(self, http_status: int, message: str, headers: dict = None):
        self.http_status = http_status
        self.message = message
        self.headers = headers

    def make_content(self) -> dict:
        """
        클라이언트로 전달할 응답용 content 생성
        :return:
        """
        return {"message": self.message}


class UserNotFound(ApiErrorBase):
    """
    User 가 없을때 처리할 예외 클래스
    """

    def __init__(self, user_id: str):
        super().__init__(http_status=status.HTTP_404_NOT_FOUND,
                         message=f"{user_id} is not existed.")


class AlreadyExistedUser(ApiErrorBase):
    """
    User 가 이미 존재할 때 처리할 예외 클래스
    """

    def __init__(self, user_id: str):
        super().__init__(http_status=status.HTTP_409_CONFLICT,
                         message=f"{user_id} is already existed.")


class ItemNotFound(ApiErrorBase):
    """
    Get요청에 대한 결과값이 없을 때 처리할 예외 클래스
    """

    def __init__(self):
        super().__init__(http_status=status.HTTP_404_NOT_FOUND,
                         message="Item not Found.")


class Unauthorized(ApiErrorBase):
    """
    UNAUTHORIZED에 대한 예외 처리 클래스
    """

    def __init__(self):
        super().__init__(http_status=status.HTTP_401_UNAUTHORIZED,
                         message="Unauthorized")


class CommanageNotFound(ApiErrorBase):
    """
    ComManage 가 없을때 처리할 예외 클래스
    """

    def __init__(self, host_id: int):
        super().__init__(http_status=status.HTTP_404_NOT_FOUND,
                         message=f"[ComManage{host_id}]  is not existed.")


class ServerError(ApiErrorBase):
    """
    서버 내에서 오류가 발생 했을 때 처리할 예외 클래스
    """

    def __init__(self, err_message: str):
        super().__init__(http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                         message=f"Server error. Internal err code : {err_message}")


class TokenInvalidate(ApiErrorBase):
    """
    token validate credentials 예외처리 클래스
    """

    def __init__(self, err_message: str):
        super().__init__(http_status=status.HTTP_401_UNAUTHORIZED,
                         message=f"toekn invalidate : {err_message}",
                         headers={"WWW-Authenticate": "Bearer"})


__all__ = (
    "UserNotFound",
    "AlreadyExistedUser",
    "ItemNotFound",
    "CommanageNotFound",
    "ServerError"
)
