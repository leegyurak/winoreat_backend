 
<h1 align="center">
  <br>
  <a href="https://winoreat.kro.kr/"><img src="https://upload.wikimedia.org/wikipedia/en/0/0e/Samsung_Lions.svg" alt="상징 타로 찾기" width="200"></a>
  <br>
  라팍 맛집 찾기 (BE)
  <br>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql" alt="MySQL">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions" alt="Github Action">
</p>

![스크린샷](https://github.com/user-attachments/assets/0740f6cf-524c-40ac-8a6f-2340bcb0cbd7)

## 주요 기능

* 맛집 등록
  - 대구 및 경산에 위치하고 라이온즈 파크와의 직선거리가 20km 이내의 맛집을 등록할 수 있습니다.
* 맛집 조회
  - 맛집의 카테고리 및 최대 거리를 조정해 라이온즈 파크 주변의 맛집을 조회할 수 있습니다.
* 주소 찾기
  - 네이버 개발자 API를 통해 해당하는 가게의 주소를 찾을 수 있습니다.
* 이미지 자동 추가
  - 네이버 개발자 API를 통해 해당하는 가게의 이미지를 찾을 수 있습니다.
* 좌표 찾기
  - 네이버 클라우드 API를 통해 해당하는 주소의 좌표와 라이온즈 파크와의 거리를 찾을 수 있습니다.

## 환경 세팅 및 실행

- [Git](https://git-scm.com), [Python](https://www.python.org/downloads/), [MySQL](https://www.mysql.com/), 그리고 [Poetry](https://python-poetry.org/)가 필요해요!

```bash
# Clone this repository
$ git clone https://github.com/leegyurak/winoreat_backend

# Go into the repository
$ cd winoreat_backend

# Enter vitual environment
$ poetry shell

# Install dependencies
$ poetry install

# Add Environment Variable
$ DJANGO_SECRET_KEY=${add your Django secret key (if env is local, do not need)}
$ MYSQL_HOST=${add your MySQL host (if env is local, do not need)}
$ MYSQL_PORT=${add your MySQL port (if env is local, do not need)}
$ MYSQL_USER=${add your MySQL user (if env is local, do not need)}
$ MYSQL_PASSWORD=${add your MySQL password (if env is local, do not need)}
$ MYSQL_DATABASE=${add your MySQL database (if env is local, do not need)}
$ ALLOW_HOSTS=${add your allow hosts}
$ ENV=${choose your environment (local, prod)}
$ NAVER_DEVELOPER_PLATFORM_CLIENT_ID=${add your naver developer platform client id}
$ NAVER_DEVELOPER_PLATFORM_CLIENT_SECRET=${add your naver developer platform client secret}
$ NAVER_CLOUD_PLATFORM_CLIENT_ID=${add your naver cloud platform client id}
$ NAVER_CLOUD_PLATFORM_CLIENT_SECRET=${add your naver cloud platform client secret}

# Run migrate
$ python manage.py migrate

# Run server
$ python manage.py runserver
```

> 도커 파일을 빌드해도 실행 가능합니다!

## 사용하기

- [라팍 맛집 찾기 접속](https://winoreat.kro.kr) 

## License

MIT

---

[issues-badge]: https://img.shields.io/github/issues/mkosir/react-parallax-tilt
[issues-url]: https://github.com/leegyurak/joatss_backend/issues
