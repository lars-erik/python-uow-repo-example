from src.core.student import Student


def test_says_hi():
    lars = Student("0001", "Lars-Erik", "Aabech", 1)
    assert lars.greet() == "Hi, Lars-Erik Aabech"