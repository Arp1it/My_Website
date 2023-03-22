from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import Contact, userProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from . forms import *
# from django.core.mail import send_mail
import smtplib
import random
from .forms import ImageForm
# from email.mime.multipart import MIMEMultipart


# Create your views here.
def index(request):
    return render(request, "maiinn/index.html")

def about(request):
    return render(request, "maiinn/about.html")

def contact(request):
    if request.method == "POST":
        # msg = MIMEMultipart()
        name = request.POST['name']
        emaill = request.POST['email']
        mesg = request.POST['message']

        # def send_mail(email, message):
        #     msg['From'] = emaill
        #     msg['To'] = email
        #     msg['Subject'] = 'contact from ... website'
        #     server = smtplib.SMTP('127.0.0.1:8000')
        #     server.sendmail(emaill,email,message.as_string())

        # email = "me@gmail.com"

        # send_mail(email, msg)

        con = Contact(name=name, email=emaill, message=mesg)
        con.save()
        messages.success(request, f"Your message has been send successfully")
        
    return render(request, "maiinn/contact.html")

# def feedback(request):
#     return render(request, "maiinn/feedback.html")

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['uname']
            email = request.POST['email']
            passs = request.POST['pass']
            # passs2 = request.POST['password2']

            if len(username) < 3 or len(username) > 15 or len(passs) < 4:
                messages.error(request, "Please enter username greater than 3 or less than 15 and password is greater than 4")
                return redirect("/signin")

            user_email_list = list(User.objects.values_list("email", flat=True))
            if email in user_email_list:
                messages.error(request, "Email address already exist")
                return redirect("/signin")

            user_list = list(User.objects.values_list("username", flat=True))
            if username in user_list:
                messages.error(request, "Username already taken")
                return redirect("/signin")

            person = User.objects.create_user(username, email, passs)
            person.save()



            identy = authenticate(username=username, password=passs)

            if identy is not None:
                auth_login(request, identy)
                messages.success(request, "Successfully Sign in.")
                profus = userProfile(user=request.user)
                profus.save()
                # print("Not Found")

                return redirect("/")
        return render(request, "maiinn/signin.html")
    
    return HttpResponse("404 - Not Found")

def login(request):
    if not request.user.is_authenticated:
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
                return redirect("/login")

        return render(request, "maiinn/login.html")

    return HttpResponse("404 - Not Found")


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
        # imgprof = userProfile.objects.filter(user=name)
        # a = userProfile(user=request.user).image
        # print(userProfile(user=request.user))
        # print(userProfile(user=request.user).image.url)
        # return render(request, "maiinn/userprofile.html", {'name':name, 'profimg':a})
        return render(request, "maiinn/userprofile.html", {'name':name})

    else:
        return HttpResponse("404-Not Found")

def Editing(request):
    if request.user.is_authenticated:
        user = request.user.Profile
        form = ImageForm(instance=user)
        name = request.user

        if request.method == "POST":
            name1 = request.POST.get('name')
            passs = request.POST['passs1']
            passs2 = request.POST['passs2']


            if passs != passs2:
                messages.error(request, "please enter confirm password correctly")
                return redirect("/change")

            if str(name) != name1:
                usersname = list(User.objects.values_list("username", flat=True))
                if name1 in usersname:
                    messages.error(request, "Username already be taken")
                    return redirect("/change")

            # if profileimg:
            form = ImageForm(request.POST, request.FILES, instance=user)
            # if form.is_valid():
            form.save()
            # return render(request, "maiinn/sdv.html", {'form':form})

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

        return render(request, "maiinn/editprofile.html", {'name':name, 'form':form})

    else:
        return HttpResponse("404-Not Found")

def forgotpasss(request):
    if not request.user.is_authenticated:
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

                        email = "me@gmail.com"
                        password = "password"
                        message = f"hello arpit your code - {codee}"
                        send_mail(email, password, message)

                        messages.success(request, f"code has been send on {i}")

                # return redirect("/verified")
                return render(request, "maiinn/verification.html", {'codee':codee})
            else:
                messages.error(request, "User not exist")
                return redirect("/forgotpasss")
        return render(request, 'maiinn/forgootpasss.html')

    return HttpResponse("404 - Not Found")


def forgot(request):
    if not request.user.is_authenticated:
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

    return HttpResponse("404 - Not Found")


def verified(request):
    if not request.user.is_authenticated:
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
    
    return HttpResponse("404 - Not Found")

# For testing new things only
# def sdv(request):
#     user = request.user.Profile
#     if request.method == "POST":
#         form = ImageForm(request.POST, request.FILES, instance=user)
#         # if form.is_valid():
#         form.save()
#     form = ImageForm(instance=user)
#     return render(request, "maiinn/sdv.html", {'form':form})