FROM python:3.12

RUN pip install poetry

COPY pyproject.toml .

COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-cache

ADD src src

ENV PYTHONPATH /src

WORKDIR src
