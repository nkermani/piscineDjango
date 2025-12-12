from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def account_view(request):
    form = AuthenticationForm()
    return render(request, "account/index.html", {"form": form})


@require_POST
def login_view(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({"success": True, "username": user.username})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "errors": "Invalid request"})


@require_POST
def logout_view(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        logout(request)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "errors": "Invalid request"})
