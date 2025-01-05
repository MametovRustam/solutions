import time
from datetime import timedelta
from functools import wraps

def retry(count=3, delay=timedelta(seconds=1), handled_exceptions=(Exception,)):
    if count < 1:
        raise ValueError
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(count):
                try:
                    return func(*args, **kwargs)
                except handled_exceptions:
                    if attempt + 1 == count:
                        raise
                    time.sleep(delay.total_seconds())
        return wrapper
    return decorator
