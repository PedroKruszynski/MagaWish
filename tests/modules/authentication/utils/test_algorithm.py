from maga_wish.modules.authentication.utils.algorithm import algorithm


def test_algorithm():
    assert algorithm() == "HS256"
