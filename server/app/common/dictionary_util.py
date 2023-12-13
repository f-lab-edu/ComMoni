def remove_none(dictionary: dict) -> dict:
    """
    dictionary에서 value값이 None인 키 삭제
    :param dictionary: 딕셔너리
    :return: None이 제거된 딕셔너리
    """

    return {key: value for key, value in dictionary.items() if value}
