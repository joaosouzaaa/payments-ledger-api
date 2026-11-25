FROM python:slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv PATH="/opt/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY . .
RUN uv sync --no-dev

CMD ["uvicorn", "ledger.main:app", "--host", "0.0.0.0", "--port", "8000"]
