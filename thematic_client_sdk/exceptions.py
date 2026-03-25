class ThematicAPIError(Exception):
    """Raised when the Thematic API returns a non-success response."""

    def __init__(self, message, status_code=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text
