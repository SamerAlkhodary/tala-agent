import logging
import time
from typing import Callable, Tuple, Type

_logger = logging.getLogger(__name__)


def retry_on_exception(func: Callable, exceptions: Tuple[Type[Exception], ...], max_retries: int = 3, delay: float = 1.0, *args, **kwargs):
    """
    Calls func(*args, **kwargs) and retry on specified exceptions with delay between tries.
    Raises on final failure.
    """
    for attempt in range(1, max_retries + 1):
        try:
            result = func(*args, **kwargs)
            return result
        except exceptions as e:
            _logger.warning(f"Attempt {attempt} failed. Retrying...: {repr(e)}")
            if attempt == max_retries:
                raise
            time.sleep(delay)
