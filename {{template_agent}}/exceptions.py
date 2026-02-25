class AnalyticsAgentError(Exception):
    """Base class for all exceptions in the Analytics Agent."""

    pass


class InputValidationError(AnalyticsAgentError):
    """Raised when the input provided is invalid."""

    def __init__(self, message: str):
        super().__init__(message)


class EngineConnectionError(AnalyticsAgentError):
    """
    Raised when the Engine Proxy service establishes a WebSocket connection,
    but fails to connect to the Qlik engine.

    The error reason and corresponding code are provided in the WebSocket message
    and close code. Typical causes include unavailable engines or authentication
    issues, but not network problems.
    """

    def __init__(
        self, message: str = None, close_code: int = None, close_msg: str = None
    ):
        super().__init__(message)
        self.close_code = close_code
        self.close_msg = close_msg

    def __str__(self):
        parts = [
            super().__str__()
            if super().__str__() != "None"
            else "EngineConnectionError: "
        ]
        if self.close_code is not None:
            parts.append(f"close_code={self.close_code}")
        if self.close_msg:
            parts.append(f"close_msg={self.close_msg}")
        return ", ".join(parts)


class NoActiveDocumentError(AnalyticsAgentError):
    """Raised when the app is not open on the selected Qlik engine but we are trying to open an Active Document on it."""

    def __init__(self, message: str = None):
        super().__init__(message)


class NetworkError(AnalyticsAgentError):
    """Raised when there is a network error."""

    def __init__(self, message: str = None, retries: int = None):
        super().__init__(message)
        self.retries = retries

    def __str__(self):
        parts = [super().__str__() if super().__str__() != "None" else "NetworkError: "]
        if self.retries is not None:
            parts.append(f"retries={self.retries}")
        return ", ".join(parts)
