import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospital_ms.settings")

from hospital_ms.wsgi import application

# uwsgi --http=0.0.0.0:8080 -w wsgi:application --static-map /assets=files/static --static-map=/media=files/media
