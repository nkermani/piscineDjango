from django.shortcuts import render
from django.conf import settings
import random
import time


def index(request):
    # Check if username exists and is still valid
    username = request.session.get("username")
    expiry = request.session.get("username_expiry")

    current_time = time.time()

    if not username or not expiry or current_time > expiry:
        # Generate new username
        username = random.choice(settings.RANDOM_USERNAMES)
        # Set expiry to 42 seconds from now
        request.session["username"] = username
        request.session["username_expiry"] = current_time + 42

    return render(request, "tips/index.html", {"username": username})
