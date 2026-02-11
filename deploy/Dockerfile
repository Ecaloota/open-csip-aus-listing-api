FROM python:3.13-slim-bookworm AS prod
WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./
COPY . .

# If a host .venv was copied, remove it
RUN rm -rf /app/.venv

ENV UV_VENV_IN_PROJECT=1
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
RUN uv sync --frozen

CMD ["/app/.venv/bin/python", "-m", "open_cec_api"]
