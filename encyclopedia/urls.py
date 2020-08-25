from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("create_wiki", views.new_wiki, name="create_wiki"),
    path("random", views.random_entry, name="random"),
    path("edit_wiki/<str:title>", views.edit_wiki, name="edit_wiki")
]
