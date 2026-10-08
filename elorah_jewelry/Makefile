.PHONY: run migrate makemigrations test shell format lint

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	pytest

shell:
	python manage.py shell

format:
	black .
	isort .

lint:
	ruff check .
