class NotAllTokensExist(Exception):
    """Raised when one or several obligatory tokens are missing."""

    def __init__(self):
        super().__init__('One or more necessary tokens are missing.')


class ResponseHasNoValidParams(Exception):
    """Raised when response does not have valid parameters."""
    pass


class TelegramSendError(Exception):
    """Raised when sending telegram message fails."""
    pass


class APIResponseError(Exception):
    """Raised when there's an error with getting API response."""
    pass


class HTTPStatusIsNotOK(Exception):
    """Raised when response HTTP Status != 200."""

    def __init__(self):
        super().__init__('Response status is not 200.')


class WrongTypeError(TypeError):
    """Raised when API response has wrong data type."""
    pass


class HomeworkStatusIsMissing(Exception):
    """Raised when the homework status is missing."""

    def __init__(self):
        super().__init__('This homework does not have any status.')


class HomeworkStatusIsNotDocumented(Exception):
    """Raised when the homework status is not documented."""

    def __init__(self):
        super().__init__('The status of this homework is not documented.')
