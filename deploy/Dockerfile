FROM python:3.12.10-slim-bookworm AS prod

# install poetry
RUN pip install poetry

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock README.md /app/src/
COPY . /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main
CMD ["/usr/local/bin/python", "-m", "open_cec_api"]

# Build new layer
FROM prod AS dev
RUN poetry install
CMD ["/usr/local/bin/python", "-m", "open_cec_api"]
