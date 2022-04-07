import re


class RequestParser:
    @staticmethod
    def is_required(is_req):
        if is_req == '1':
            return 'Y'
        else:
            return 'F'

    @staticmethod
    def close_condition_mark(close_value):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", close_value) is not None:
            return 'D'
        elif re.match(r"^[1-9]\d*$", close_value) is not None:
            return 'C'
        else:
            return 'N'
