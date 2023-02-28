from django.contrib import admin
from django.urls import path, include
from maiinn import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("feedback", views.feedback, name="feedback"),
    path("signin", views.signin, name="signin"),
    path("login", views.login, name="login"),
    path("handlelogout", views.handlelogout, name="handlelogout"),
    path("handlelogout", views.handlelogout, name="handlelogout"),
    path("Profile", views.Profile, name="Profile"),
    path("change", views.Editing, name="change"),
]
