from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.user_entry, name="user_entry"),
    path("find/", views.find, name="find"),
    path("new_article/", views.add_article, name="add_article"),
    path("edit_page/", views.edit_page, name="edit_page"),
    path("random/",views.random_page,name="random_page")
]
