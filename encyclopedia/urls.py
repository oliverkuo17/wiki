from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_entry, name="get_entry"),
    path("search", views.get_search, name="search"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("wiki/<str:title>/edit", views.editEntry, name="editEntry"),
    path("random", views.get_random, name="get_random")
]
