class APIError(Exception):
    """Base class for all API errors."""

    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code


class Timeout(APIError):
    """Raised when timeout exceeded while getting soup."""

    def __init__(self, message="Timeout exceeded while doing the HTTP request, check your internet connection."):
        super().__init__(message, status_code=504)


class DecodeError(APIError):
    """Raised when error occurred while decoding soup."""

    def __init__(self, message="Error occurred while decoding the weather data."):
        super().__init__(message, status_code=500)


class InvalidCityError(APIError):
    """Raised when invalid city name is given."""

    def __init__(self, message="Invalid city name."):
        super().__init__(message, status_code=400)

# @AmarnathCJD
