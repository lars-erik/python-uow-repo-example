import pytest

from src.core.student import Student
from src.db import UnitOfWork, Repository

unitOfWork = UnitOfWork('sqlite:///students.db')


@pytest.fixture()
def uow():
    unitOfWork.recreate_database()
    yield unitOfWork
    unitOfWork.remove_database()

def test_crud_lifecycle(uow):
    repo = Repository(uow, Student, "student_number")
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

def test_crud_query(uow):
    repo = Repository(uow, Student, "student_number")
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

