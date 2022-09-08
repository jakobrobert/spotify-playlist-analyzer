import sys
import traceback


class HttpError(Exception):
    # TODO CLEANUP after all occurrences adjusted, remove message from constructor
    def __init__(self, status_code, message, title="", traceback_items=None):
        if traceback_items is None:
            traceback_items = []

        self.status_code = status_code
        self.message = message
        self.title = title
        self.traceback_items = traceback_items

    @staticmethod
    def from_last_exception():
        # ex_value contains less info than traceback and no additional info, so can ignore this
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_name = ex_type.__name__

        # Using this instead so the template code can deal with formatting
        # With traceback.format_exc()
        traceback_items = traceback.extract_tb(ex_traceback)

        return HttpError(502, "", ex_name, traceback_items)

