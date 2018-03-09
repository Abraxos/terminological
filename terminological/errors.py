class Error(Exception):
    """Base class for exceptions in terminological."""
    pass

class UnknownOutlineTypeError(Error):
    """Exception raised when an unknown outline type is introduced into the code."""

    def __init__(self, message):
        self.message = message
