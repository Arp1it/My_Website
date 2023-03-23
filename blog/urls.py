from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path("blogcomment", views.blogcomment, name="blogcomment"),
    path("search", views.search, name="search"),
    
    path("", views.bloghome, name="bloghome"),
    path("Postblog", views.Postblog, name="Postblog"),
    path("delet", views.delet, name="delet"),
    path("editpost", views.editpost, name="editpost"),
    path("newwpos", views.newwpos, name="newwpos"),
    path("comdel", views.comdel, name="comdel"),
    path("<str:slug>", views.blogpost, name="blogpost"),
]
