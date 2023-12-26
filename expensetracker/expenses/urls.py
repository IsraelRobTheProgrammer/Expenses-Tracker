from . import views
from django.urls import path


urlpatterns = [
    path("", views.index, name="expenses_homepage"),
    path("add_expenses", views.add_expenses, name="add_expenses"),
    path("search_expenses", views.search_expenses, name="search_expenses"),
    path("edit_expenses/<int:id>", views.edit_expenses, name="edit_expenses"),
    path("delete_expenses/<int:id>", views.delete_expenses, name="delete_expenses"),
    path(
        "expenses_category_summary",
        views.expenses_category_summary,
        name="expenses_category_summary",
    ),
    path("view_stats", views.stats_view, name="stats"),
]
