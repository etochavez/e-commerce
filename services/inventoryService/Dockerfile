FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=50051

WORKDIR /home/app
COPY ./pyproject.toml ./poetry.lock* ./
COPY ./protobuf ./protobuf

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

RUN python3 -m grpc_tools.protoc -I ./protobuf --python_out=. --grpc_python_out=. inventory.proto

CMD [ "python", "main.py" ]