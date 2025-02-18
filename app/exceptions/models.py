
class AIPolicingException(Exception):
    """This is the base class for all AIPolicing errors"""

    def __init__(self, status_code: int, message: str, resolution: str = None):
        self.status_code = status_code
        self.message = message
        self.resolution = resolution
        super().__init__(message)

class CustomError(AIPolicingException):
    """User has provided an invalid or expired token"""

    def __init__(self, status_code: int, message: str, resolution: str = None):
        super().__init__(status_code, message, resolution)
    def __str__(self):
        return f"CustomError(status_code={self.status_code}, message={self.message}, resolution={self.resolution})"