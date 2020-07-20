from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("add", views.add, name="add"),
    path("search", views.search, name="search"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random")
]