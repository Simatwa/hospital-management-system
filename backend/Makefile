.PHONY: install setup developmentsuperuser runserver runserver-prod default

default: install setup developmentsuperuser runserver-api

install:
	pip install -r requirements.txt

setup:
	python manage.py makemigrations users hospital finance external staffing

	python manage.py migrate

	python manage.py collectstatic --no-input


developmentsuperuser:
	python manage.py createsuperuser --username developer \
	 --email developer@localhost.domain --noinput

runserver:
	python manage.py runserver

runserver-prod:
	uwsgi --http=0.0.0.0:8080 -w wsgi:application --static-map /static=files/static --static-map=/media=files/media

runserver-api:
	python -m api run api