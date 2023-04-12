from django.contrib import admin
from django.urls import path, include
from maiinn import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    # path("feedback", views.feedback, name="feedback"),
    path("signin", views.signin, name="signin"),
    path("loin", views.login, name="login"),
    path("handlelogout", views.handlelogout, name="handlelogout"),
    path("Profile", views.Profile, name="Profile"),
    path("change", views.Editing, name="change"),
    path("forgotpasss", views.forgotpasss, name="forgotpasss"),
    path("forgot", views.forgot, name="forgot"),
    path("verified", views.verified, name="verified"),
    # path("sdv", views.sdv, name="sdv"),
]
