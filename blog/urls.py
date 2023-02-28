from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path("blogcomment", views.blogcomment, name="blogcomment"),
    
    path("", views.bloghome, name="bloghome"),
    path("<str:slug>", views.blogpost, name="blogpost"),
]
