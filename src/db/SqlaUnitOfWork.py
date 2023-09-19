from src.core.UnitOfWork import UnitOfWork
from src.db.DatabaseInitializer import DatabaseInitializer


class SqlaUnitOfWork(UnitOfWork):

    def __init__(self):
        self.session = DatabaseInitializer.create_session()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()