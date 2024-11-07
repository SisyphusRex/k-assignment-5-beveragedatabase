"""Program Exception Definitions"""

# Walter Podewil
# CIS 226
# November 6, 2024


class AlreadyImportedError(Exception):
    """Exception to raise when CSV file already imported"""

    pass  # pylint:disable=W0107


class AlreadyCreatedDatabaseError(Exception):
    """Exception to raise when Database already created"""

    pass  # pylint:disable=W0107
