# django-streamlit-dashboard
Example of how to make Streamlit Dashboards of Django Apps


## Project Install
To install the project, simply run:
```
make install
```
It will create a virtual environment inside a `.venv` folder and install the project dependencies. 

## Database Initialization
To init the Databse, simply run:
```
make init_database
```
It will:
- create a sqlite database file in the project root
- apply the migrations
- create a superuser (username: `admin`, password: `admin`)
- load fake data inside the database

## Running the project

### Monitor your Database with Streamlit
To start the streamlit dashboard, simply run:
```
make start_database_monitoring
```

### Start the django server
To start the Django server, simply run:
```
make start_django_server
```
then go to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to access Django Admin website.