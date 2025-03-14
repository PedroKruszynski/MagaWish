FROM python:3.12

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

COPY pyproject.toml alembic.ini /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync

ENV PYTHONPATH=/app

COPY ./maga_wish /app/maga_wish

CMD ["uvicorn", "maga_wish.shared.infra.http.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]