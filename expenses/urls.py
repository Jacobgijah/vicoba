from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("", views.index, name="expenses"),
    path("add-expense/", views.add_expense, name="add-expenses"),
    path("search-expenses", csrf_exempt(views.search_expenses), name="search-expenses"),
    path("edit-expense/<int:id>", views.expense_edit, name="expense_edit"),
    path("expense-delete/<int:id>", views.delete_expense, name="expense-delete"),
    path("loan_category_summary", views.loan_category_summary, name="loan_category_summary"),
    path("stats", views.stats_view, name="stats"),
]
