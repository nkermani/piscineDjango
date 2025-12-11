#!/bin/bash
python3 manage.py makemigrations ex00
python3 manage.py migrate
python3 manage.py loaddata ex00/fixtures/data.json
python3 manage.py runserver
