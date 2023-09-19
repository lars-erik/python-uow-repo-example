from src.core import Student


def test_student_greeting():
    """
    This test is here to show that we have a "pure" test testing "pure" logic on the domain entity.
    """

    # Arrange
    lars = Student("0001", "Lars-Erik", "Aabech", 1)

    # Act / Assert
    assert lars.greet() == "Hi, Lars-Erik Aabech"