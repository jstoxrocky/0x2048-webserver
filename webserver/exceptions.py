class InvalidUsage(Exception):
    status_code = 500

    def __init__(self):
        Exception.__init__(self)


class PaymentLocatorPayloadValidationError(InvalidUsage):
    message = 'PaymentLocatorPayloadValidationError'


class UnpaidSessionValidationError(InvalidUsage):
    message = 'UnpaidSessionValidationError'


class PaymentError(InvalidUsage):
    message = 'PaymentError'


class MovePayloadValidationError(InvalidUsage):
    message = 'MovePayloadValidationError'


class PaidSessionValidationError(InvalidUsage):
    message = 'PaidSessionValidationError'
