FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.5.1

RUN mkdir /app/

WORKDIR /app/

COPY . .

RUN poetry install --no-root

EXPOSE 8005

ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0:8005", "joatss.wsgi:application", "--workers", "4"]