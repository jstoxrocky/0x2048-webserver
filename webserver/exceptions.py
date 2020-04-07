class InvalidUsage(Exception):
    status_code = 500

    def __init__(self):
        Exception.__init__(self)


class SignaturePayloadValidationError(InvalidUsage):
    message = 'SignaturePayloadValidationError'


class UnpaidSessionValidationError(InvalidUsage):
    message = 'UnpaidSessionValidationError'


class PaymentError(InvalidUsage):
    message = 'PaymentError'


class MoveValidationError(InvalidUsage):
    message = 'MoveValidationError'


class PaidSessionValidationError(InvalidUsage):
    message = 'PaidSessionValidationError'
