SHELL := /bin/bash

install:
	python -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt
	source .venv/bin/activate && pre-commit install

start_django_server:
	source .venv/bin/activate && cd classificationapp && python manage.py runserver

start_database_monitoring:
	source .venv/bin/activate && cd classificationapp && streamlit run annotationsdatabase/st_annotations_monitoring.py