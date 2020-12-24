class SubprocessServerManagerBaseException(Exception):
    pass


class ImproperlyConfigured(SubprocessServerManagerBaseException):
    pass


class SubprocessServerNotResponding(SubprocessServerManagerBaseException):
    pass

class ServerCannotConnect(SubprocessServerManagerBaseException):
    pass
