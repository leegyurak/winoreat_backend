from exceptions import (
    InvalidDisplayValueException,
    IncorrectQueryRequestException,
    InvalidStartValueException,
    InvalidSortValueException,
    MalformedEncodingException,
    UnknownNaverException,
    AuthenticationFailedException,
    InvalidSearchAPIException,
    SystemErrorException,
    InvalidParameterException,
    InvalidRequestException,
    ApplicationAuthenticationFailedException,
    NotFoundException,
    InternalServerErrorException,
)


class RestaurantExceptionHandler:
    @staticmethod
    def handle_search_exceptions(exception: Exception) -> Exception:
        exception_mapping = {
            (
                InvalidDisplayValueException,
                IncorrectQueryRequestException,
                InvalidStartValueException,
                InvalidSortValueException,
                MalformedEncodingException,
                UnknownNaverException,
            ): InvalidRequestException,
            AuthenticationFailedException: ApplicationAuthenticationFailedException,
            InvalidSearchAPIException: NotFoundException,
            SystemErrorException: InternalServerErrorException,
        }

        for exception_types, mapped_exception in exception_mapping.items():
            if isinstance(exception, exception_types):
                return mapped_exception(str(exception))

        return exception

    @staticmethod
    def handle_geocode_exceptions(exception: Exception) -> Exception:
        if isinstance(exception, InvalidParameterException):
            return InvalidRequestException(str(exception))
        elif isinstance(exception, SystemErrorException):
            return InternalServerErrorException(str(exception))
        return exception
