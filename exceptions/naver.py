class NaverClientException(Exception):
    pass


class IncorrectQueryRequestException(NaverClientException):
    pass


class InvalidDisplayValueException(NaverClientException):
    pass


class InvalidStartValueException(NaverClientException):
    pass


class InvalidSortValueException(NaverClientException):
    pass


class InvalidSearchAPIException(NaverClientException):
    pass


class MalformedEncodingException(NaverClientException):
    pass


class SystemErrorException(NaverClientException):
    pass


class UnknownNaverException(NaverClientException):
    pass


class AuthenticationFailedException(NaverClientException):
    pass


class InvalidParameterException(NaverClientException):
    pass
