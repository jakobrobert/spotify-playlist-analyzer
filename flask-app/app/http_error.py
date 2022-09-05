import sys
import traceback


class HttpError(Exception):
    # TODO CLEANUP after all occurrences adjusted, remove message from constructor
    def __init__(self, status_code, message, name="", traceback_lines=[]):
        self.status_code = status_code
        self.message = message
        self.name = name
        self.traceback_lines = traceback_lines

    @staticmethod
    def from_last_exception():
        # Somehow, if then printing ex_traceback, just prints something like <traceback object at 0x7f43916de7c8>,
        # So using traceback.format_exc() for this.
        # ex_value just contains less info traceback, so can ignore this
        ex_type, ex_value, ex_traceback = sys.exc_info()
        ex_name = ex_type.__name__
        traceback_text = traceback.format_exc()
        # TODO improve formatting, proper indentation -> can retrieve info from traceback and format manually using extract_tb, see here:
        #  https://stackoverflow.com/questions/4690600/python-exception-message-capturing
        # then can handle proper indentation in the HTML template
        # should NOT replace newlines and spaces by HTML tags in python code, this would be ugly
        traceback_lines = traceback_text.splitlines()

        return HttpError(502, "", ex_name, traceback_lines)

