import pytest

from src.core import Repository, UnitOfWork, Student
from src.db import SqlaUnitOfWork, SqlaRepository, DatabaseInitializer

DatabaseInitializer.initialize('sqlite:///students.db')

@pytest.fixture()
def uow() -> UnitOfWork:
    DatabaseInitializer.recreate_database()
    unitOfWork = SqlaUnitOfWork()
    yield unitOfWork
    unitOfWork.close()
    DatabaseInitializer.remove_database()

@pytest.fixture()
def repo(uow) -> Repository:
    return SqlaRepository(uow, Student, "student_number")

def test_crud_lifecycle(uow: UnitOfWork, repo: Repository):
    """
    This is a special type of test where we ignore the Arrange, Act, Assert pattern.
    The reason is that we want these four things to be tested in sequence on a fresh database.
    The asserts "really" test the "one thing" that we can "Create, Read, Update, Delete" entities.
    One such test should be enough for all entities since configuration errors will be
    handled by individual use-case centered integration tests en masse.
    This test's prime directive is to verify that our UnitOfWork and Repository implementations have the basics in place.
    """
    # create
    lars = Student("0001", "Lars-Erik", "Aabech", 1)
    repo.create(lars)
    uow.commit()

    # verify creation
    larsFromDb = repo.read("0001")
    assert (larsFromDb.first_name == "Lars-Erik" and
            larsFromDb.year == 1)

    # mutate
    lars.year = 2
    repo.update(lars)
    uow.commit()

    # verify mutation
    larsFromDb = repo.read("0001")
    assert larsFromDb.year == 2

    # remove
    repo.delete(lars)
    uow.commit()

    # verify removal
    larsFromDb = repo.read("0001")
    assert larsFromDb == None

def test_crud_query(uow: UnitOfWork, repo: Repository):
    """
    This test verifies that we can use a "generic repository" with type-specific criterias when querying
    TODO: Trace the SQL to see that the predicate is really translated to SQL
    """
    # Arrange
    repo.create(Student("0001", "Lars-Erik", "Aabech", 1))
    repo.create(Student("0002", "Mats", "Lindh", 2))
    repo.create(Student("0003", "Arne", "Normann", 2))
    uow.commit()

    # Act
    second_year_students = repo.query(Student.year == 2)

    # Assert
    student_names = set(map(lambda x: x.first_name, second_year_students))
    assert student_names == { "Mats", "Arne" }

