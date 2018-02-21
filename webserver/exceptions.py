class InvalidUsage(Exception):
    status_code = 500

    def __init__(self):
        Exception.__init__(self)


class NoGameStarted(InvalidUsage):
    message = 'NoGameStarted'


class ValidationError(InvalidUsage):
    message = 'ValidationError'


class UnexpectedPreimage(InvalidUsage):
    message = 'UnexpectedPreimage'


class UnexpectedSigner(InvalidUsage):
    message = 'UnexpectedSigner'


class IOUPaymentTooLow(InvalidUsage):
    message = 'IOUPaymentTooLow'


class PaymentRequired(InvalidUsage):
    message = 'PaymentRequired'
