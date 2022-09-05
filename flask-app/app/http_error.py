import sys
import traceback


class HttpError(Exception):
    # TODO CLEANUP after all occurences adjusted, remove message from constructor
    def __init__(self, status_code, message, name=None, traceback_text=None):
        self.status_code = status_code
        self.message = message
        self.name = name
        self.traceback_text = traceback_text

    @staticmethod
    def from_last_exception():
        # Somehow, if then printing ex_traceback, just prints something like <traceback object at 0x7f43916de7c8>,
        # So using traceback.format_exc() for this.
        # ex_value just contains less info traceback, so can ignore this
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_name = ex_type.__name__
        traceback_text = traceback.format_exc()

        return HttpError(502, "", ex_name, traceback_text)

