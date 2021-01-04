[![Build Status](https://travis-ci.com/etiennody/mutadi.svg?branch=main)](https://travis-ci.com/etiennody/mutadi)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Mutadi
======

App built for project 13 in Python Developer path at OpenClassrooms.

Mutadi is a platform that creates a link between those who need free help and those who are willing to help close to home and without commitment. Mutadi reconstitute the informal mutual aid that once existed in villages between generations.
Originally, Mutadi is a Latin contraction of "mutuum adiutorium" which means mutual help.


## Online application
In progress...

## Requirements
* Python 3
* Django
* Django-ckeditor
* Psycopg2
* PostgreSQL
* Requests
* Pillow

## Setup
To run this application locally:

* Create a virtual environment. First, install pipenv:
    ```
    pip install --user pipenv
    ```

* Clone / create the application repository:
    ```
    git clone https://github.com/etiennody/mutadi.git && cd mutadi


* Copy and update environment variables values in .env:
    ```
     cp .env.example .env
    ```

* Install the requirements:
    ```
    pipenv install
    ```

* Activate the pipenv shell:
    ```
    pipenv shell
    ```

* Create a database with PostgreSQL
    ```

* Run Mutadi application:
    ```
    python manage.py runserver
    ```

* Launch Django server:
You can visit localhost at https://127.0.0.1:8000/

* Enjoy!
