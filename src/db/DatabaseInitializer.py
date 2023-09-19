import os

from sqlalchemy import MetaData, Table, Column, String, Integer, PrimaryKeyConstraint, create_engine
from sqlalchemy.orm import registry, sessionmaker

from src.core.student import Student


class DatabaseInitializer:
    metadata = None
    engine = None
    session_maker = None

    @classmethod
    def initialize(cls, connection_string):
        if cls.metadata is None:
            cls.connection_string = connection_string
            cls.engine = create_engine(connection_string)
            cls.session_maker = sessionmaker(bind=cls.engine)
            cls.metadata = MetaData()
            student_table = Table(
                'students',
                cls.metadata,
                Column('student_number', String, primary_key=True),
                Column('first_name', String),
                Column('last_name', String),
                Column('year', Integer)
            )
            PrimaryKeyConstraint('student_number', name='PK_students')

            registry().map_imperatively(Student, student_table, primary_key=student_table.c.student_number)

    @classmethod
    def create_session(cls):
        return cls.session_maker()

    @classmethod
    def create_database(cls):
        cls.metadata.create_all(cls.engine)

    @classmethod
    def remove_database(cls):
        cls.metadata.drop_all(cls.engine)
        cls.engine.dispose()
        path = cls.connection_string.replace('sqlite:///', '')
        if os.path.exists(path):
            os.remove(path)

    @classmethod
    def recreate_database(cls):
        cls.remove_database()
        cls.create_database()