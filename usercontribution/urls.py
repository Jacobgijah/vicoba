from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("", views.index, name="contribution"),
    path("contribution_source_summary", views.contribution_source_summary, name="contribution_source_summary"),
    path("cstats", views.cstats_view, name="cstats"),
    # path("add-expense/", views.add_contribution, name="add-contibution"),
    # path("search-contibution", csrf_exempt(views.search_contibution), name="search-contibution"),
    # path("edit-contibution/<int:id>", views.contibution_edit, name="contibution_edit"),
    # path("contibution-delete/<int:id>", views.delete_expense, name="contibution-delete"),
]
 