import base64


class TokenUtilError(Exception):
    pass


class TokenUtil:
    KEY_USER_ID = "user_id"
    KEY_HOST_ID = "host_id"
    CHAR_SET = "utf-8"

    def __init__(self, file_path):
        self.token = ""
        self.payload = {}
        self.file_path = file_path

    def read_file(self):
        try:
            with open(self.file_path, "r", encoding=self.CHAR_SET) as file:
                self.token = file.readline()
        except OSError as err:
            raise TokenUtilError(err)

    def write_file(self):
        if self.token == "":
            raise TokenUtilError(f"token is empty")

        try:
            with open(self.file_path, "w", encoding=self.CHAR_SET) as file:
                file.write(self.token)
        except OSError as err:
            raise TokenUtilError(err)

    def parse_payload(self):
        if self.token == "":
            raise TokenUtilError(f"token is empty")

        encode_payload = self.token.split(".")[1]
        byte_payload = base64.b64decode(encode_payload)
        payload = byte_payload.decode(self.CHAR_SET)
        self.payload = eval(payload)

    def set_token(self, token: str):
        self.token = token

    def get_host_id(self) -> int:
        host_id = self.payload.get(self.KEY_HOST_ID)

        if not host_id:
            raise TokenUtilError(f"host_id is invalid")

        return int(host_id)

    def get_user_id(self) -> str:
        user_id = self.payload.get(self.KEY_USER_ID)

        if not user_id:
            raise TokenUtilError(f"user_id is invalid")

        return user_id
