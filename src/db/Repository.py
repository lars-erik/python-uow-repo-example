class Repository():

    def __init__(self, session, entity_class, primary_key):
        self.session = session
        self.entity_class = entity_class
        self.primary_key = primary_key

    def create(self, entity):
        self.session.add(entity)

    def read(self, id):
        return self.session.query(self.entity_class).filter(getattr(self.entity_class, self.primary_key) == id).first()

    def update(self, entity):
        self.session.merge(entity)

    def delete(self, entity):
        self.session.delete(entity)

