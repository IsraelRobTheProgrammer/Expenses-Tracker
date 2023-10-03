from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("register", views.reg_view, name="register"),
    path("validate_username", csrf_exempt(views.user_val_view), name="user_val"),
]
