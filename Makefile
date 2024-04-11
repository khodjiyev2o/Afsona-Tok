#!/usr/bin/make



hello:
	echo "Hello, Afsona"
run:
	export DJANGO_SETTINGS_MODULE=core.settings.develop
	daphne -b 0.0.0.0 -p 8000  core.asgi:application
migrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
createsuperuser:
	python3 manage.py createsuperuser
test:
	pytest -vv -s

ocpp_service:
	uvicorn ocpp_service.main:app --host 0.0.0.0 --port 8080 --workers 3




## -B disable(pycache), -vv(show more information), -s(show print statements)

