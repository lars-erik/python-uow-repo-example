class Repository:
    """
    A repository mimics a collection of objects while at the same time
    handling the physical storage and retrieval of entities.
    Implementations handle the specifics of such storage and retrieval.
    However, this "interface" to storage is ever-green no matter what
    mechanisms we use to actually persist and retrieve data.
    """
    def create(self, entity):
        """
        Persists a new entity. Make sure to provide a unique key.
        :param entity: The new entity
        :return: None
        """
        pass
    def update(self, entity):
        """
        Updates the data of the entity with the same primary key
        :param entity: The entity to update
        :return: None
        """
        pass
    def delete(self, entity):
        """
        Removes the entity with the same primary key
        :param entity: The entity to remove
        :return: None
        """
        pass
    def read(self, id):
        """
        Returns the entity witht the same primary key, if any
        :param id: The primary key of the entity
        :return: The entity if any
        """
        return None
    def query(self, *args, **kwargs):
        """
        Returns a list of entities matching the predicate
        :param args: A predicate, for instance student_year==2
        :param kwargs:
        :return: A list of entities matching the specified predicate
        """
        return []