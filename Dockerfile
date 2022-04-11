# pull official base image
FROM python:3.10

# set work directory
WORKDIR /app
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="${PATH}:/root/.local/bin"

# install dependencies
RUN curl -sSL https://install.python-poetry.org | python - \
    && poetry update \
    && poetry install

CMD [ "poetry", "run", "python", "app.py" ]