#!/bin/bash

# Apply database migrations
echo "Applying migrations..."
python3 manage.py makemigrations
python3 manage.py makemigrations chat
python3 manage.py makemigrations account
python3 manage.py migrate

# Initialize Users
if [ -f "init_users.py" ]; then
    echo "Initializing users..."
    python3 manage.py shell < init_users.py
else
    echo "init_users.py not found!"
fi

# Initialize Rooms
if [ -f "init_rooms.py" ]; then
    echo "Initializing rooms..."
    python3 manage.py shell < init_rooms.py
else
    echo "init_rooms.py not found!"
fi

echo "Initialization complete."

echo "Starting server..."
python3 manage.py runserver
