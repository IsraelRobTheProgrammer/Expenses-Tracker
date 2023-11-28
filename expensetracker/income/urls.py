from . import views
from django.urls import path


urlpatterns = [
    path("", views.index, name="income_homepage"),
    path("add_income", views.add_income, name="add_income"),
    path("search_income", views.search_income, name="search_income"),
    path("edit_income/<int:id>", views.edit_income, name="edit_income"),
    path("delete_income/<int:id>", views.delete_income, name="delete_income"),
]
