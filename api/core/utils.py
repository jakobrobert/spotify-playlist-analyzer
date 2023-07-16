import functools
import time


class Utils:
    @staticmethod
    def measure_execution_time(log_prefix):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                response = func(*args, **kwargs)
                end_time = time.time()
                elapsed_time_seconds = end_time - start_time
                elapsed_time_ms = elapsed_time_seconds * 1000
                # TODONOW revert
                #print(f"[Execution time] {log_prefix}{func.__name__} => {elapsed_time_ms} ms")
                return response

            return wrapper

        return decorator
