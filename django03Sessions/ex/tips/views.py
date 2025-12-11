from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.utils import timezone
from .forms import RegistrationForm, LoginForm, TipForm
from .models import Tip
import random


def get_anonymous_username(request):
    username = request.session.get("username")
    expiry = request.session.get("username_expiry")
    current_time = timezone.now().timestamp()

    if not username or not expiry or current_time > expiry:
        username = random.choice(settings.RANDOM_USERNAMES)
        request.session["username"] = username
        request.session["username_expiry"] = current_time + 42
    return username


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == "POST":
            form = TipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user
                tip.save()
                return redirect("index")
        else:
            form = TipForm()
    else:
        username = get_anonymous_username(request)
        form = None

    tips = Tip.objects.all().order_by("-date")
    return render(
        request, "tips/index.html", {"username": username, "tips": tips, "form": form}
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    username = get_anonymous_username(request)

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, "tips/register.html", {"form": form, "username": username})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    username = get_anonymous_username(request)

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return redirect("index")
    else:
        form = LoginForm()
    return render(request, "tips/login.html", {"form": form, "username": username})


def logout_view(request):
    logout(request)
    return redirect("index")


def vote_tip(request, tip_id, vote_type):
    if not request.user.is_authenticated:
        return redirect("index")

    try:
        tip = Tip.objects.get(id=tip_id)
    except Tip.DoesNotExist:
        return redirect("index")

    user = request.user

    if vote_type == "up":
        if user in tip.upvotes.all():
            tip.upvotes.remove(user)
        else:
            tip.upvotes.add(user)
            tip.downvotes.remove(user)
    elif vote_type == "down":
        if (
            user.reputation >= 15 or user == tip.author
        ):  # Assuming author can always vote on their own tip? No, prompt says "Un utilisateur débloquera l’autorisation de downvoter les Tips autres que les siens à partir de 15 points de réputation". It implies for others. Can they downvote their own? Usually yes or no. Let's assume the restriction applies to "Tips autres que les siens". So if user == tip.author, they can downvote? Or maybe they can't vote on their own tips at all? The prompt doesn't forbid voting on own tips. But usually you can't. Let's stick to the prompt: "Un utilisateur débloquera l’autorisation de downvoter les Tips autres que les siens à partir de 15 points de réputation". This implies they can downvote their own tips? Or maybe they can't downvote their own tips at all? Let's assume the restriction is: IF tip.author != user AND user.reputation < 15 THEN cannot downvote.
            if user != tip.author and user.reputation < 15:
                return redirect("index")

            if user in tip.downvotes.all():
                tip.downvotes.remove(user)
            else:
                tip.downvotes.add(user)
                tip.upvotes.remove(user)

    return redirect("index")


def delete_tip(request, tip_id):
    if not request.user.is_authenticated:
        return redirect("index")

    try:
        tip = Tip.objects.get(id=tip_id)
        # Check permissions
        # Can delete if author OR (reputation >= 30 AND tip is not theirs)
        if request.user == tip.author or (
            request.user.reputation >= 30 and request.user != tip.author
        ):
            tip.delete()
    except Tip.DoesNotExist:
        pass

    return redirect("index")
