from django.shortcuts import render
from django.conf import settings
from .forms import HistoryForm
import datetime
import os


def ex02(request):
    history = []
    if os.path.exists(settings.LOG_FILE_PATH):
        with open(settings.LOG_FILE_PATH, "r") as f:
            history = [line.strip() for line in f.readlines()]

    if request.method == "POST":
        form = HistoryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} : {entry}"

            with open(settings.LOG_FILE_PATH, "a") as f:
                f.write(log_entry + "\n")

            history.append(log_entry)
    else:
        form = HistoryForm()

    return render(request, "ex02/form.html", {"form": form, "history": history})
