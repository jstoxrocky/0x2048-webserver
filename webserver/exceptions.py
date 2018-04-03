class InvalidUsage(Exception):
    status_code = 500

    def __init__(self):
        Exception.__init__(self)


class ValidationError(InvalidUsage):
    message = 'ValidationError'


class UnexpectedPaymentAttempt(InvalidUsage):
    message = 'UnexpectedPaymentAttempt'


class UnexpectedNonceGenerationAttempt(InvalidUsage):
    message = 'UnexpectedNonceGenerationAttempt'


class UnexpectedEmptyNonce(InvalidUsage):
    message = 'UnexpectedEmptyNonce'


class UnexpectedContractNonce(InvalidUsage):
    message = 'UnexpectedContractNonce'


class UnexpectedMoveAttemptWithoutPaying(InvalidUsage):
    message = 'UnexpectedMoveAttemptWithoutPaying'
