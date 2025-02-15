# filepath: /home/karnad1/Sandbox/Projects/mammothon2025/backend/Dockerfile
FROM ghcr.io/astral-sh/uv:bookworm-slim

WORKDIR /app
RUN uv sync

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]