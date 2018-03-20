
FROM arm32v6/python:3.6-alpine3.6
LABEL Name=viajes Version=0.0.1

ENV PROJECT_DIR=/app
ENV PIPENV_TIMEOUT=9000
ENV PYTHONPATH=:/app

WORKDIR $PROJECT_DIR

RUN pip install pipenv

COPY Pipfile* $PROJECT_DIR/

RUN pipenv install

COPY . $PROJECT_DIR/

RUN cp $PROJECT_DIR/credentials/maps.py $PROJECT_DIR/maps/api_credentials.py

CMD ["pipenv", "run", "python", "main.py", "--logdir", "logs", "--env", "production"]
