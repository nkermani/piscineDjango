from django.shortcuts import render

# Create your views here.


def django_page(request):
    return render(request, "django.html")


def affichage_page(request):
    return render(request, "affichage.html")


def templates_page(request):
    return render(request, "templates.html")
