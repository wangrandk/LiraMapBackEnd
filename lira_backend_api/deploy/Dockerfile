FROM python:3.9.6-slim-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN apt-get -y install apt-utils

RUN pip install -U pip setuptools

RUN pip install poetry==1.1.13

# Configuring poetry
RUN poetry config virtualenvs.create true

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install

# Copying actuall application
COPY . /app/src/
RUN poetry install

CMD ["/usr/local/bin/python", "-m", "lira_backend_api"]
