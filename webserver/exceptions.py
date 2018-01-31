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
