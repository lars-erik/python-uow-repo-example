from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, registry

from src.core.student import Student
from src.db.Repository import Repository


def test_crud_lifecycle():
    engine = create_engine('sqlite:///students.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    student_table = Table(
        'students',
        metadata,
        Column('student_number', String, primary_key=True),
        Column('first_name', String),
        Column('last_name', String),
        Column('year', Integer)
    )
    PrimaryKeyConstraint('student_number', name='PK_students')

    metadata.drop_all(engine)
    metadata.create_all(engine)

    registry().map_imperatively(Student, student_table, primary_key=student_table.c.student_number)
    metadata.reflect(bind=engine)

    repo = Repository(session, Student, "student_number")
    lars = Student("0001", "Lars-Erik", "Aabech", 1)

    repo.create(lars)
    session.commit()

    larsFromDb = repo.read("0001")
    assert larsFromDb.first_name == "Lars-Erik"
    assert larsFromDb.year == 1

    lars.year = 2
    repo.update(lars)
    session.commit()

    larsFromDb = repo.read("0001")
    assert larsFromDb.year == 2

    repo.delete(lars)
    session.commit()

    larsFromDb = repo.read("0001")
    assert larsFromDb == None