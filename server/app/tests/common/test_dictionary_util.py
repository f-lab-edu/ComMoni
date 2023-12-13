from app.common.dictionary_util import remove_none


class TestDictionaryUtil:

    def test_success_1(self):
        test_dict = {"a": 1, "b": 2}

        assert test_dict == remove_none(test_dict)

    def test_success_2(self):
        test_dict = {"a": 1, "b": 2, "c": None}
        result = {"a": 1, "b": 2}

        assert result == remove_none(test_dict)

    def test_success_3(self):
        test_dict = {}

        assert test_dict == remove_none(test_dict)

    def test_success_4(self):
        test_dict = {"a": None, "b": None}

        assert {} == remove_none(test_dict)
