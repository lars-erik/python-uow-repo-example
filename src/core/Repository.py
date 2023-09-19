class Repository:
    """
    Implementations handle the storage and retrieval of entities
    """
    def create(self, entity):
        """
        Persists a new entity. Make sure to provide a unique key.
        :param entity: The new entity
        :return: None
        """
        pass
    def update(self, entity): pass
    def delete(self, entity): pass
    def read(self, id): return None
    def query(self, *args, **kwargs): return []