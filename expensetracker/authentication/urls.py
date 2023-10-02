from . import views
from django.urls import path


urlpatterns = [
    path("register", views.reg_view, name="register"),
]
