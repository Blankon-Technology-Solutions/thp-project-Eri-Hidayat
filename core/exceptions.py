class APIException(Exception):
    def __init__(self, code, message):
        self.message = message
        self.code = code


class APIAccessDenied(APIException):
    def __init__(
        self, code="access_denied", message="Invalid or missing authorization."
    ):
        self.message = message
        self.code = code


class APINotFound(APIException):
    def __init__(self, code="not_found", message="Not found."):
        self.message = message
        self.code = code


class APIForbidden(APIException):
    def __init__(self, code="forbidden", message="Forbidden."):
        self.message = message
        self.code = code


class APIConflict(APIException):
    def __init__(self, code="conflict", message="Conflict."):
        self.message = message
        self.code = code
