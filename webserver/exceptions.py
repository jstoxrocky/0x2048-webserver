class InvalidUsage(Exception):
    status_code = 500

    def __init__(self):
        Exception.__init__(self)


class AddressPayloadValidationError(InvalidUsage):
    message = 'AddressPayloadValidationError'


class UnpaidSessionValidationError(InvalidUsage):
    message = 'UnpaidSessionValidationError'


class PaymentError(InvalidUsage):
    message = 'PaymentError'


class MoveValidationError(InvalidUsage):
    message = 'MoveValidationError'


class PaidSessionValidationError(InvalidUsage):
    message = 'PaidSessionValidationError'
