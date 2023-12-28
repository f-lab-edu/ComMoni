from aiohttp import FormData


class LoginData:
    """
    로그인 데이터 생성
    """

    def __init__(self, username: str, password: str):
        """
        로그인 정보
        """
        self.username = username
        self.password = password

    def make(self):
        """
        데이터를 form data 형태로 변환
        """
        form_data = FormData()
        form_data.add_field("username", self.username)
        form_data.add_field("password", self.password)
        form_data.add_field("temp_login", True)

        return form_data
