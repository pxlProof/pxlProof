FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
# COPY . .
RUN ls -lah
RUN uv sync

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "18012"]