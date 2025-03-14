docker compose run --rm app alembic revision -m "create users table"

docker compose run --rm app alembic upgrade head

cp .env.example .env

uv sync after uv venv after source .venv/bin/activate

coverage run --source=app -m pytest
coverage report --show-missing
coverage html --title "coverage_maga_wish"