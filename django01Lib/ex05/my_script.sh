#!/usr/bin/env bash

pip --version
if ! pip --version > /dev/null 2>&1; then
    echo "pip is not installed. Please install pip to proceed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "django_venv" ]; then
    python3 -m venv django_venv
fi

source django_venv/bin/activate

pip install --upgrade pip > /dev/null 2>&1
pip install -r requirement.txt > /dev/null 2>&1

pip list

# Create Django project if it doesn't exist
if [ ! -d "Django" ]; then
    django-admin startproject Django
fi

cd Django

# Create helloworld app if it doesn't exist
if [ ! -d "helloworld" ]; then
    python manage.py startapp helloworld
fi

cd ..

echo "Django project created successfully!"
echo "To run the server:"
echo "  source django_venv/bin/activate"
echo "  cd Django"
echo "  python3 manage.py runserver"
echo ""
echo "Then visit: http://localhost:8000/helloworld"
