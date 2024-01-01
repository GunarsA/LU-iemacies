# Iemacies.lv

Roadmap learning platform in Django.

## About

The app's development was focused on learning the Django framework and its features. So the front end design is without any styling and is meant to be used only as example of the backend functionality.

## Requirements

- Python 3.12
- PostgreSQL 16

## Installation (Tested on Windows 11)

1. Setup the **postgresql** database
2. Clone the repository and navigate to the project folder
3. Create a virtual environment `python -m venv venv`
4. Install the dependencies `pip install -r requirements.txt`
5. Create a .env file using the .env.example file
6. Run the migrations `python manage.py migrate`
7. Seed the database `python manage.py loaddata fixtures.json`
8. Run the server `python manage.py runserver`

## Usage

Web application is available at <http://localhost:8000/>

Admin user can be created with `python manage.py createsuperuser`

Admin panel is available at <http://localhost:8000/admin/>
