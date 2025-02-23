import time
from logger import log
from functools import wraps


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        log.info('Function: {}, Time: {:.9f} s'.format(func.__name__, end - start))
        return result

    return wrapper


def sleep(duration):
    log.info(f'Sleeping for {duration}sec..')
    time.sleep(duration)


def show_progress(total_iterations):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # Call the original function
            for i, item in enumerate(result, start=1):
                progress = (i / total_iterations) * 100
                log.debug(f"Progress: {progress:.2f}%")
            return result

        return wrapper

    return decorator
