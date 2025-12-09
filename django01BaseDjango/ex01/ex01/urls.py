from django.urls import path
from . import views

urlpatterns = [
    path("django", views.django_page, name="django"),
    path("affichage", views.affichage_page, name="affichage"),
    path("templates", views.templates_page, name="templates"),
]
