
FROM python:3.5.5-alpine3.4
LABEL Name=viajes Version=0.0.1

ENV PROJECT_DIR=/app

WORKDIR $PROJECT_DIR

RUN pip install pipenv

RUN pipenv --python 3.5.5

COPY Pipfile* $PROJECT_DIR

RUN pipenv install

COPY . $PROJECT_DIR

CMD ["pipenv", "run", "python", "main.py", "logs"]