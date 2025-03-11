docker compose run --rm app alembic revision -m "create users table"

docker compose run --rm app alembic upgrade head