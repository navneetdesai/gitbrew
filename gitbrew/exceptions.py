class InvalidAnswerFormatException(Exception):
    """
    Raised when the answer does not follow expected format
    or does not match expected regex pattern
    """

    pass


class InvalidRepositoryException(Exception):
    """
    Raised when the repository is invalid
    """

    pass
