#!/bin/bash
python3 ex/manage.py makemigrations ex/tips
python3 ex/manage.py migrate
python3 ex/manage.py runserver
