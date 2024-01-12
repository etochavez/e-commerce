FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=50051

WORKDIR /home/app
COPY ./pyproject.toml ./poetry.lock* ./
COPY ./protobuf ./protobuf
COPY ./infra-scripts ./infra-scripts

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

RUN ["chmod", "+x", "./infra-scripts/ggen"]
RUN ./infra-scripts/ggen

CMD [ "python", "main.py" ]