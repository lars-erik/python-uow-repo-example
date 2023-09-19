from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, registry

from src.core.student import Student


class UnitOfWork():

    def __init__(self, connection_string='sqlite:///students.db'):
        self.engine = create_engine(connection_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = MetaData()
        student_table = Table(
            'students',
            self.metadata,
            Column('student_number', String, primary_key=True),
            Column('first_name', String),
            Column('last_name', String),
            Column('year', Integer)
        )
        PrimaryKeyConstraint('student_number', name='PK_students')

        registry().map_imperatively(Student, student_table, primary_key=student_table.c.student_number)
        self.metadata.reflect(bind=self.engine)

    def create_database(self):
        self.metadata.create_all(self.engine)

    def remove_database(self):
        self.metadata.drop_all(self.engine)

    def recreate_database(self):
        self.remove_database()
        self.create_database()

    def commit(self):
        self.session.commit()
