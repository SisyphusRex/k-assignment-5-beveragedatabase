"""Program Exception Definitions"""




class AlreadyImportedError(Exception):
    """Exception to raise when CSV file already imported"""

    pass  # pylint:disable=W0107


class AlreadyCreatedDatabaseError(Exception):
    """Exception to raise when Database already created"""

    pass  # pylint:disable=W0107


class DatabaseNotCreatedError(Exception):
    """exception to raise if database not created"""

    pass  # pylint:disable=W0107
