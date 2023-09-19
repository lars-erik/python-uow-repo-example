import pytest

from src.core.Repository import Repository
from src.core.UnitOfWork import UnitOfWork
from src.core.student import Student
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
def student_repo(uow) -> Repository:
    return SqlaRepository(uow, Student, "student_number")

def test_crud_lifecycle(uow: UnitOfWork, repo: Repository):
    lars = Student("0001", "Lars-Erik", "Aabech", 1)

    repo.create(lars)
    uow.commit()

    larsFromDb = repo.read("0001")
    assert larsFromDb.first_name == "Lars-Erik"
    assert larsFromDb.year == 1

    lars.year = 2
    repo.update(lars)
    uow.commit()

    larsFromDb = repo.read("0001")
    assert larsFromDb.year == 2

    repo.delete(lars)
    uow.commit()

    larsFromDb = repo.read("0001")
    assert larsFromDb == None

def test_crud_query(uow: UnitOfWork, repo: Repository):
    lars = Student("0001", "Lars-Erik", "Aabech", 1)
    mats = Student("0002", "Mats", "Lindh", 2)
    arne = Student("0003", "Arne", "Normann", 2)
    repo.create(lars)
    repo.create(mats)
    repo.create(arne)
    uow.commit()

    second_year_students = repo.query(Student.year == 2)

    student_names = set(map(lambda x: x.first_name, second_year_students))
    assert student_names == { "Mats", "Arne" }

