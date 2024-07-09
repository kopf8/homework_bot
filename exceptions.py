class NotAllTokensExist(Exception):
    """Raised when one or several obligatory tokens are missing."""
    pass


class ResponseHasNoValidParams(Exception):
    """Raised when response does not have valid parameters."""
    pass


class TelegramSendError(Exception):
    pass


class APIResponseError(Exception):
    """Raised when response HTTP Status != 200."""
    pass


class HTTPStatusIsNotOK(Exception):
    """Raised when response HTTP Status != 200."""
    pass


class WrongTypeError(TypeError):
    """Raised when API response has wrong data type."""
    pass


class HomeworkStatusIsNotDocumented(Exception):
    """Raised when the homework status is not documented."""
    pass
