FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=50051

# Copy the application code to the container image
WORKDIR /usr/src/app

# Install application dependencies
COPY ./pyproject.toml ./poetry.lock* ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

# Expose the gRPC port
EXPOSE $PORT

# Copy the program source files
COPY . .

# Compile the gRPC protobuf files
RUN ["chmod", "+x", "./infra-scripts/ggen"]
RUN ./infra-scripts/ggen

#CMD [ "python", "main.py" ]