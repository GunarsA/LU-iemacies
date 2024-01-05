# Iemacies

Private teacher search platform

## About

The app's development was focused on learning the Django framework and its features. Design was added using **django-tailwind**.
## Features

- User roles (student, teacher, admin)
- Users can only modify their own data, for example, students can only edit their own applications

### Guest

- View subjects, teacher, adverts and reviews
- Register and login

### Logged in user

- View and edit profile
- Chat with related users (those with whom there is an open application)

### Student

- Create and edit applications
- Create and edit reviews only for finished applications

### Teacher

- Create and edit adverts
- Approve and reject applications

### Admin

- Create and edit subjects using **Django admin panel**
- Give and remove teacher role using **Django admin panel**

## Requirements

- Python
- PostgreSQL
- Node.js
- npm

## Installation (Tested on Windows 11)

1. Setup the **postgresql** database
   1. Install **postgresql**
   2. Create a user
   3. Create a database
2. Clone the repository and navigate to the project folder
3. Setup python virtual environment
   1. Create the environment `python -m venv venv`
   2. Activate the environment `venv\Scripts\activate`
   3. Install the dependencies `pip install -r requirements.txt`
4. Create a .env file using the .env.example file
5. Run the migrations `python manage.py migrate`
6. Seed the database `python manage.py loaddata fixtures.json`
7. Install the **django-tailwind** dependencies `python manage.py tailwind install`
8. Run the **django-tailwind** development server `python manage.py tailwind start`
9. Run the server `python manage.py runserver`

## Usage

Web application is available at <http://localhost:8000/>

Admin panel is available at <http://localhost:8000/admin/>

There are 3 users (student, teacher, admin) with the password **password** for each of them. You can login with any of them or create a new user.

## Commands for development

- To save dependencies `pip freeze > requirements.txt`
- To save database state to fixture file `python -Xutf8 manage.py dumpdata main auth.user auth.group -o  fixtures_new.json`

## Screenshots

### Student's profile detail page

![Student's profile detail page](screenshots/profile_detail_student.png)

### Teacher's profile detail page

![Teacher's profile detail page](screenshots/profile_detail_teacher.png)

### Chat detail page

![Chat detail page](screenshots/chat_detail.png)

### Subject list page

![Subject list page](screenshots/subject_list.png)

### Subject detail page

![Subject details page](screenshots/subject_detail.png)

### Advert list page

![Advert list page](screenshots/advert_list.png)

### Student's advert detail page

![Student's advert detail page](screenshots/advert_detail_student.png)

### Teacher's advert detail page

![Teacher's advert detail page](screenshots/advert_detail_teacher.png)

### Advert create page

![Advert create page](screenshots/advert_create.png)
