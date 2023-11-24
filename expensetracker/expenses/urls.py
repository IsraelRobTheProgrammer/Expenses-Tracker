from . import views
from django.urls import path


urlpatterns = [
    path("", views.index, name="expenses_homepage"),
    path("add_expenses", views.add_expenses, name="add_expenses"),
    path("edit_expenses/<int:id>", views.edit_expenses, name="edit_expenses"),
    path("delete_expenses/<int:id>", views.delete_expenses, name="delete_expenses"),
]
