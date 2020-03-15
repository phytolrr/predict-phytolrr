
class ValidationError(Exception):
    def __init__(self, message, detail=None):
        self.message = message
        self.detail = detail


class ErrorCode(object):
    PARA_NOT_EXISTS = "The parameter {} does not exists"
    INVALID_PARA = "The parameter {} is invalid: {}"
    OBJECT_NOT_EXISTS = "Does not exits: {}"
    OFFSET_OVERLAP = "The offset is overlapped with current motifs"
    OFFSET_EXISTS_WRONG = "The offset has been marked wrong previously, you can unmark it directly"
