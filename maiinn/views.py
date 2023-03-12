from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from . forms import *
# from django.core.mail import send_mail
import smtplib
import random


# Create your views here.
def index(request):
    return render(request, "maiinn/index.html")

def about(request):
    return render(request, "maiinn/about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mesg = request.POST['message']

        con = Contact(name=name, email=email, message=mesg)
        con.save()
        messages.success(request, "Successfully Send")
        
    return render(request, "maiinn/contact.html")

def feedback(request):
    return render(request, "maiinn/feedback.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['uname']
        email = request.POST['email']
        passs = request.POST['pass']
        # passs2 = request.POST['password2']

        if len(username) < 3 or len(username) > 15 or len(passs) < 4:
            messages.error(request, "Please enter username greater than 3 or less than 15 and password is greater than 4")
            return redirect("/")

        user_email_list = list(User.objects.values_list("email", flat=True))
        if email in user_email_list:
            messages.error(request, "Email address already exist")
            return redirect("/")

        user_list = list(User.objects.values_list("username", flat=True))
        if username in user_list:
            messages.error(request, "Username already taken")
            return redirect("/")

        person = User.objects.create_user(username, email, passs)
        person.save()

        identy = authenticate(username=username, password=passs)

        if identy is not None:
            auth_login(request, identy)
            messages.success(request, "Successfully Sign in.")

            return redirect("/")
    return render(request, "maiinn/signin.html")

def login(request):
    if request.method == "POST":
        loginname = request.POST['luname']
        loginpassword = request.POST['lpass']

        identifyuser = authenticate(username=loginname, password=loginpassword)

        if identifyuser is not None:
            auth_login(request, identifyuser)
            messages.success(request, "Successfully Logged in.")
            return redirect("/")

        else:
            messages.error(request, "This account is not register please go and signin.")
            return redirect("/")

    return render(request, "maiinn/login.html")


def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully Logout")
        return redirect("/")

    else:
        return HttpResponse("404 - Not Found")


def Profile(request):
    if request.user.is_authenticated:
        name = request.user
        return render(request, "maiinn/userprofile.html", {'name':name})

    else:
        return HttpResponse("404-Not Found")

def Editing(request):
    if request.user.is_authenticated:
        name = request.user
        if request.method == "POST":
            name1 = request.POST.get('name')
            passs = request.POST['passs1']
            passs2 = request.POST['passs2']

            if passs != passs2:
                messages.error(request, "please enter confirm password correctly")
                return redirect("/change")

            u = User.objects.get(username__exact=name)
            u.username = name1
            u.set_password(passs)
            u.save()

            userchangeidenty = authenticate(username=name1, password=passs)

            if userchangeidenty is not None:
                auth_login(request, userchangeidenty)
                messages.success(request, "changed Successfully")

            else:
                messages.error(request, "username or password already have been taken")

            return redirect("/Profile")

        return render(request, "maiinn/editprofile.html", {'name':name})

    else:
        return HttpResponse("404-Not Found")

def forgotpasss(request):
    if request.method == 'POST':
        emmail = request.POST['email']

        email_list = list(User.objects.values_list("email", flat=True))
        user_list = list(User.objects.values_list("username", flat=True))
        print(email_list, user_list)

        codee = random.randint(11111, 99999)

        if emmail in email_list:
            for i in email_list:
                if i == emmail:
                    def send_mail(email, password, message):
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()
                        server.login(email, password)
                        server.sendmail(email, i, message)

                    email = "your_gmail"
                    password = "your_password"
                    message = f"hello arpit your code - {codee}"
                    send_mail(email, password, message)

                    messages.success(request, f"code has been send on {i}")

            # return redirect("/verified")
            return render(request, "maiinn/verification.html", {'codee':codee})
        else:
            messages.error(request, "User not exist")
            return redirect("/forgotpasss")
    return render(request, 'maiinn/forgootpasss.html')


def forgot(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        confirmpass = request.POST['confirm-password']

        user_names = list(User.objects.values_list("username", flat=True))
        if name not in user_names:
            messages.error(request, "User not exist")
            return redirect("/forgot")

        if password != confirmpass:
            messages.error(request, "password and confirm password not matched")
            return redirect("/forgot")

        usrr = User.objects.get(username__exact=name)
        usrr.set_password(password)
        usrr.save()

        messages.success(request, "Successfully change password")
        return redirect("/login")
    return render(request, "maiinn/forgot.html")


def verified(request):
    if request.method == "POST":
        user_code = request.POST['code']
        user_codee = request.POST['codee']
        print(user_codee)

        if user_code == user_codee:
            return redirect("/forgot")

        else:
            messages.error(request, "Code is wrong")
            return redirect("/forgotpass")

    return render(request, "maiinn/verification.html")
