from datetime import datetime, timezone
import json
from utils.logger import setup_logger

logger = setup_logger("error_utils")


class AppError(Exception):
    """Custom application error that can be raised across services."""

    def __init__(self, source: str, error: Exception | str, data: dict | None = None, status_code: int = 500):
        self.source = source
        self.error = str(error) if isinstance(error, Exception) else error
        self.data = data
        self.status_code = status_code
        self.timestamp = datetime.now(timezone.utc).isoformat()
        super().__init__(self.error)

    def to_dict(self) -> dict:
        return {
            "status": "error",
            "source": self.source,
            "data": self.data,
            "message": self.error,
            "timestamp": self.timestamp,
        }


def format_error(source: str, error: Exception | str, data: dict | None = None, raise_exc: bool = False) -> dict:
    """
    Format errors into a standard structure. Optionally raise AppError.

    Args:
        source (str): The source of the error.
        error (Exception | str): The error to format.
        data (dict | None): Optional payload.
        raise_exc (bool): If True, raises AppError instead of returning dict.

    Returns:
        dict: Standardized error dictionary (if raise_exc=False).
    """
    app_error = AppError(source, error, data)

    # Always log the dict form
    logger.error(json.dumps(app_error.to_dict()))

    if raise_exc:
        raise app_error

    return app_error.to_dict()