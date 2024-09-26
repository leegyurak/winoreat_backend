class InvalidRequestException(Exception):
    """400"""
    pass


class ApplicationAuthenticationFailedException(Exception):
    """403"""
    pass


class NotFoundException(Exception):
    """404"""
    pass


class InternalServerErrorException(Exception):
    """500"""
    pass


class AlreadyAddRestaurantException(Exception):
    """3일 안에 해당 식당을 추가한 내역이 있음"""
    pass


class CategoryNotFoundException(Exception):
    """존재하지 않는 카테고리"""
    pass
