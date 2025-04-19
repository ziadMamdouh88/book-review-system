Book Review System
Django Online Bookstore
A web-based bookstore built with Django and Django REST Framework. Users can browse books, read content, and submit their own reviews.

Contents
Overview

Features

Tech Stack

Installation

Project Structure

API Overview

Database Models

Authentication

Testing

Security

Future Improvements

Overview
This platform provides a RESTful backend for managing an online bookstore. Users can register, log in, browse books, read details and content, and submit reviews. Admins have full control over the system through a dedicated admin panel.

Features
User Accounts

Register, login, and manage profiles

Token-based authentication

Book Catalog

View available books

Read detailed descriptions and content

Filter and search by title, author, genre, or ISBN

Review System

Submit, edit, or delete reviews

View ratings and comments by other users

Admin Panel

Add and manage books, users, and reviews

Tech Stack
Backend: Django 4.2, Django REST Framework 3.14

Database: PostgreSQL 13

Authentication: Token-based

Containerization: Docker + Docker Compose

Testing: pytest, pytest-django, pytest-cov

Additional Tools: django-filter, django-cors-headers

Installation
Using Docker
Clone the repository

bash
Copy
Edit
git clone https://github.com/ziadMamdouh88/book-review-system.git
cd book-review-system
Build and run the containers

docker-compose up --build
Create a superuser


docker-compose exec web python manage.py createsuperuser
Seed the database with sample books

docker-compose exec web python manage.py seed_books
Manual Setup
Clone the repository and navigate into it

Create a virtual environment and activate it

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

pip install -r requirements.txt
Add environment variables (optional if using .env)

Apply migrations

python manage.py makemigrations
python manage.py migrate
Create a superuser and seed the database

python manage.py createsuperuser
python manage.py seed_books
Start the development server

python manage.py runserver
Visit:

API: http://localhost:8000/api/

Admin: http://localhost:8000/admin/

Project Structure

book-review-system/
├── bookstore/            # Django project settings
├── books/                # Main app (models, views, APIs)
├── manage.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
API Overview
Authentication

POST /api/auth/token/ — Get auth token

Add token to headers as: Authorization: Token your-token

Users

GET /api/users/ (admin)

POST /api/users/ — Register

GET /api/users/me/ — Get current user info

Books

GET /api/books/ — List all books (with search/filter options)

GET /api/books/<id>/ — Book details

POST /api/books/ — Add book (admin only)

Reviews

GET /api/reviews/ — All reviews

POST /api/reviews/ — Add review

GET /api/reviews/my_reviews/ — My reviews

PUT /api/reviews/<id>/ — Update review

DELETE /api/reviews/<id>/ — Delete review

Database Models
User

id, email, username, first_name, last_name, is_active, is_staff, date_joined

Book

id, title, author, description, isbn, genre, price, content, publication_date

Review

id, book (FK), user (FK), rating, comment, created_at, updated_at

Authentication
Token-based authentication is used.
To access secured endpoints:

Send your credentials to /api/auth/token/

Use the returned token in headers:
Authorization: Token your-token
Testing

Run tests inside Docker:
docker-compose exec web pytest

Or without Docker:
pytest

Check test coverage:
pytest --cov=books --cov-report=html
Security
Custom user model with email-based login

Strong password policies

Permissions for user actions

CSRF protection and input validation

CORS and security headers in production

UUIDs to protect user and object IDs

Future Improvements
Add caching

Social login (Google, Facebook)

Frontend interface (React or Vue)

Book recommendations

Wishlist and favorite lists

Review analytics and charts

Notifications for new content

