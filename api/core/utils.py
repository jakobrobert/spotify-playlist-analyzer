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
                print(f"[Execution time] {log_prefix}{func.__name__} => {elapsed_time_ms} ms")
                return response

            return wrapper

        return decorator

    @staticmethod
    def get_request_arg_as_int_or_none(request_args, name):
        value_string = request_args.get(name)

        if not value_string:
            return None

        try:
            return int(value_string)
        except ValueError:
            return None
