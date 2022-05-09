SHELL := /bin/bash

install:
	python -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt
	source .venv/bin/activate && pre-commit install

start_django_server:
	source .venv/bin/activate && cd classificationapp && python manage.py runserver

start_database_monitoring:
	source .venv/bin/activate && cd classificationapp && streamlit run annotationsdatabase/st_annotations_monitoring.py

init_database:
	source .venv/bin/activate && cd classificationapp && python manage.py migrate
	DJANGO_SUPERUSER_PASSWORD="admin" source .venv/bin/activate && cd classificationapp && python manage.py createsuperuser --noinput --username admin --email admin@admin.com
	make load_fake_data

load_fake_data:
	source .venv/bin/activate && cd classificationapp && python manage.py loadannotations
