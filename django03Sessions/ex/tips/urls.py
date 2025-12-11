from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("vote/<int:tip_id>/<str:vote_type>/", views.vote_tip, name="vote_tip"),
    path("delete/<int:tip_id>/", views.delete_tip, name="delete_tip"),
]
