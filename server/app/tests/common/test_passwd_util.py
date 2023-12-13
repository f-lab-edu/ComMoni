from app.common.passwd_util import verify_password, get_password_hash


class TestPasswdUtil:

    def test_success_1(self):
        plain_pwd = "1234"

        hashed_pwd = get_password_hash(password=plain_pwd)

        assert verify_password(plain_password=plain_pwd, hashed_password=hashed_pwd)

    def test_success_2(self):
        plain_pwd = "1234"
        hashed_pwd = get_password_hash(password=plain_pwd)

        other_passwd = "1235"
        assert not verify_password(plain_password=other_passwd, hashed_password=hashed_pwd)
