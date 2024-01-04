FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/app
COPY ./pyproject.toml ./poetry.lock* ./

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]