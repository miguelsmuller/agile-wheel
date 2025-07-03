class ApiError(Exception):
    def __init__(self, message, cause=None, extra=None):
        super().__init__(message)

        self.message = message
        self.cause = cause
        self.extra = extra or {}

    def __str__(self):
        return self.message
