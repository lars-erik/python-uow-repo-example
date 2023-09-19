class UnitOfWork:
    """
    A Unit of Work is used to execute recorded actions against entities
    in the persistence medium. If anythin goes wrong, the entire series
    of operations can be rolled back.
    The Unit of Work is also responsible to release any locks made on
    any system resources that need to be managed.
    """
    def commit(self):
        """
        Ensures that all operations are executed in the persistence medium
        :return: None
        """
        pass

    def close(self):
        """
        Releases any resources locked by the persistence medium
        :return: None
        """
        pass