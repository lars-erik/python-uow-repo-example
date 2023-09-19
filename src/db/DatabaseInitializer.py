import os

from sqlalchemy import MetaData, Table, Column, String, Integer, PrimaryKeyConstraint, create_engine
from sqlalchemy.orm import registry, sessionmaker

from src.core.Student import Student


class DatabaseInitializer:
    """
    This is the main ingredient in separating domain entities from the ORM.
    Everything we'd otherwise put inside the entity is declared here.
    The upside is that the metadata instance can be exposed to feed
    for instance view models with GUI validation information.
    The bigger upside is that the entities are pure and free to be stored _anywhere_.
    """
    metadata = None
    engine = None
    session_maker = None

    @classmethod
    def initialize(cls, connection_string):
        """
        Sets up everything SQLAlchemy needs to map between the database and the entities.
        Including what's needed to create connections and transactions with our selected database.
        :param connection_string: A full ODBC connection string. For instance sqllite:///filename.db
        """
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
        """
        Creates a new connection and transction to the database
        :return: A SQLAlchemy Session
        """
        return cls.session_maker()

    @classmethod
    def create_database(cls):
        """
        Creates the required tables in the database
        :return: None
        """
        cls.metadata.create_all(cls.engine)

    @classmethod
    def remove_database(cls):
        """
        Removes all tables from the database and finally the database file
        :return: None
        """
        cls.metadata.drop_all(cls.engine)
        cls.engine.dispose()
        path = cls.connection_string.replace('sqlite:///', '')
        if os.path.exists(path):
            os.remove(path)

    @classmethod
    def recreate_database(cls):
        """
        Removes the database completely and recreates it
        :return: None
        """
        cls.remove_database()
        cls.create_database()