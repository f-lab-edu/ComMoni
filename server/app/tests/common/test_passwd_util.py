from app.common.passwd_util import PasswdUtil


class TestPasswdUtil:

    def test_success_1(self):
        plain_pwd = "1234"

        hashed_pwd = PasswdUtil.get_hash(password=plain_pwd)

        assert PasswdUtil.verify(plain=plain_pwd, hashed=hashed_pwd)

    def test_success_2(self):
        plain_pwd = "1234"
        hashed_pwd = PasswdUtil.get_hash(password=plain_pwd)

        other_passwd = "1235"
        assert not PasswdUtil.verify(plain=other_passwd, hashed=hashed_pwd)
