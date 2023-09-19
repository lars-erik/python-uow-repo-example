from src.core.Repository import Repository


class SqlaRepository(Repository):

    def __init__(self, uow, entity_class, primary_key):
        self.uow = uow
        self.entity_class = entity_class
        self.primary_key = primary_key

    def create(self, entity):
        self.uow.session.add(entity)

    def update(self, entity):
        self.uow.session.merge(entity)

    def delete(self, entity):
        self.uow.session.delete(entity)

    def read(self, id):
        return self.uow.session.query(self.entity_class).filter(getattr(self.entity_class, self.primary_key) == id).first()

    def query(self, *args, **kwargs):
        return self.uow.session.query(self.entity_class).filter(*args, **kwargs)

