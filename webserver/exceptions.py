class InvalidUsage(Exception):
    status_code = 500

    def __init__(self):
        Exception.__init__(self)


class UnknownMove(InvalidUsage):
    message = 'UnknownMove'


class MissingUser(InvalidUsage):
    message = 'MissingUser'


class NoGameStarted(InvalidUsage):
    message = 'NoGameStarted'


class UnexpectedDataFormat(InvalidUsage):
    message = 'UnexpectedDataFormat'


class UnexpectedDataType(InvalidUsage):
    message = 'UnexpectedDataType'


class UnexpectedPreimage(InvalidUsage):
    message = 'UnexpectedPreimage'


class UnexpectedSigner(InvalidUsage):
    message = 'UnexpectedSigner'


class IOUPaymentTooLow(InvalidUsage):
    message = 'IOUPaymentTooLow'
