from src.core.UnitOfWork import UnitOfWork
from src.db.DatabaseInitializer import DatabaseInitializer


class SqlaUnitOfWork(UnitOfWork):
    """
    A SQLAlchemy-specific UnitOfWork implementation
    """

    def __init__(self):
        self.session = DatabaseInitializer.create_session()

    def commit(self):
        """
        A SQLAlchemy specific implementation of the commit method
        :return: None
        """
        self.session.commit()

    def close(self):
        """
        Closes the SQLAlchemy session behind the implementation-specific Unit of Work
        :return:
        """
        self.session.close()