#!/usr/bin/make



hello:
	echo "Hello, Afsona"
run:
	python3 manage.py runserver 0.0.0.0:8000
migrations:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate
createsuperuser:
	python3 manage.py createsuperuser
test:
	pytest -vv -s

ocpp_service:




## -B disable(pycache), -vv(show more information), -s(show print statements)

