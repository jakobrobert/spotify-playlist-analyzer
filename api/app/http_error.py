import sys
import traceback


class HttpError(Exception):
    def __init__(self, status_code, title, message="", traceback_items=None):
        if traceback_items is None:
            traceback_items = []

        self.status_code = status_code
        self.title = title
        self.message = message
        self.traceback_items = traceback_items

    @staticmethod
    def from_last_exception():
        # ex_value contains less info than traceback and no additional info, so can ignore this
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_name = ex_type.__name__
        ex_message = str(ex_value)

        # Using this instead so the template code can deal with formatting
        # With traceback.format_exc()
        traceback_items = traceback.extract_tb(ex_traceback)

        return HttpError(502, ex_name, ex_message, traceback_items)

