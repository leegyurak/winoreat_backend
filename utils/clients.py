from enum import Enum
from typing import Any, Final, NoReturn

import requests
from django.conf import settings
from requests import Response

from exceptions import NaverClientException, IncorrectQueryRequestException, InvalidSearchAPIException, InvalidDisplayValueException, InvalidSortValueException, InvalidStartValueException, MalformedEncodingException, SystemErrorException, UnknownNaverException, AuthenticationFailedException, InvalidParameterException


class NaverURLType(Enum):
    CLOUD_PLATFORM = 'https://naveropenapi.apigw.ntruss.com/'
    DEVELOPER_PLATFORM = 'https://openapi.naver.com/'
    
    
class NaverExceptionHandler:
    ERROR_MAP: dict[str, NaverClientException] = {
        'SE01': IncorrectQueryRequestException('잘못된 쿼리요청입니다.'),
        'SE02': InvalidDisplayValueException('부적절한 display 값입니다.'),
        'SE03': InvalidStartValueException('부적절한 start 값입니다.'),
        'SE04': InvalidSortValueException('부적절한 sort 값입니다.'),
        'SE05': InvalidSearchAPIException('존재하지 않는 검색 api 입니다.'),
        'SE06': MalformedEncodingException('잘못된 형식의 인코딩입니다.'),
        'SE99': SystemErrorException('네이버 서버에 문제가 발생했습니다.'),
        '024': AuthenticationFailedException('API Key를 확인해주세요'),
        'INVALID_REQUEST': InvalidParameterException('요청 파라미터 값이 잘못 되었습니다.'),
        'SYSTEM_ERROR': SystemErrorException('네이버 서버에 문제가 발생했습니다.'),
    }

    @classmethod
    def raise_exception(cls, error_code: str) -> NoReturn:
        exception_class = cls.ERROR_MAP.get(error_code, UnknownNaverException('알 수 없는 에러가 발생했습니다.'))
        raise exception_class(f"Naver API Error: {error_code}")


class NaverClient:
    def __init__(self) -> None:
        self.develop_platform_client_id: str = settings.NAVER_DEVELOPER_PLATFORM_CLIENT_ID
        self.develop_platform_client_secret: str = settings.NAVER_DEVELOPER_PLATFORM_CLIENT_SECRET
        self.cloud_platform_client_id: str = settings.NAVER_PLATFORM_PLATFORM_CLIENT_ID
        self.cloud_platform_client_secret: str = settings.NAVER_PLATFORM_PLATFORM_CLIENT_SECRET

    def _is_search_places(self, endpoint: str) -> True:
        if endpoint == 'v1/search/local.json' or endpoint == 'v1/search/image.json':
            return True
        return False
    
    def _create_full_url(self, url_type: NaverURLType, endpoint: str) -> str:
        return f'{url_type.value}{endpoint}'

    def _make_request(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        if self._is_search_places(endpoint=endpoint):
            full_url: str = self._create_full_url(NaverURLType.DEVELOPER_PLATFORM, endpoint)
            headers: dict[str, str] = {
                'X-Naver-Client-Id': self.develop_platform_client_id,
                'X-Naver-Client-Secret': self.develop_platform_client_secret,
            }
        else:
            full_url = self._create_full_url(NaverURLType.CLOUD_PLATFORM, endpoint)
            headers = {
                'X-NCP-APIGW-API-KEY-ID': self.cloud_platform_client_id,
                'X-NCP-APIGW-API-KEY': self.cloud_platform_client_secret,
            }

        response: Response = requests.get(full_url, headers=headers, params=params)
        res_dict: dict[str, Any] = response.json()

        if not response.ok:
            NaverExceptionHandler.raise_exception(res_dict['errorCode'] if res_dict.get('errorCode') else res_dict.get('errorMessage'))

        return res_dict

    def search_places(self, name: str, display: int = 5) -> list[dict[str, Any]]:
        ENDPOINT: Final[str] = 'v1/search/local.json'
        params: dict[str, Any] = {
            'query': name,
            'display': display,
        }
        result: dict[str, Any] = self._make_request(ENDPOINT, params)
        return result['items']
    
    def get_images(self, name: str, display: int = 2) -> list:
        ENDPOINT: Final[str] = 'v1/search/image.json'
        params: dict[str, Any] = {
            'query': name,
            'display': display,
        }
        result: dict[str, Any] = self._make_request(ENDPOINT, params)
        return result['items']
    
    def get_geocode_distance_by_address(self, address: str) -> tuple[str, str, float]:
        ENDPOINT: Final[str] = 'map-geocode/v2/geocode'
        params: dict[str, Any] = {
            'query': address,
            'coordinate': '128.6812364,35.8411290',
        }
        result: dict[str, Any] = self._make_request(ENDPOINT, params)
        return result['addresses'][0].get('x'), result['addresses'][0].get('y'), result['addresses'][0].get('distance')
