from src.db.DatabaseInitializer import DatabaseInitializer


class UnitOfWork():

    def __init__(self):
        self.session = DatabaseInitializer.create_session()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()