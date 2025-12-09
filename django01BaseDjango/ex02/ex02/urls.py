from django.urls import path
from . import views

urlpatterns = [
    path("", views.ex02, name="ex02"),
]
