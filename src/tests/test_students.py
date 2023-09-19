from src.core import Student


def test_says_hi():
    # Arrange
    lars = Student("0001", "Lars-Erik", "Aabech", 1)

    # Act / Assert
    assert lars.greet() == "Hi, Lars-Erik Aabech"