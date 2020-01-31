from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import re
import bcrypt
import random
from django.http import JsonResponse

# Create your views here.
def index(request):
    context = {
        "user" : User.objects.get(id=request.session["user_id"]),
        "all_users" : User.objects.exclude(id=request.session["user_id"]),
    }
    return render(request,'base.html', context)
def display_about_us(request):
    return render(request,'about_us.html')
def display_contact_us(request):
    return render(request,'contact_us.html')
def display_registration(request):
    return render(request, 'registration.html')

def process_registration(request):

    errors = User.objects.user_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/registration/')
    else:
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
        user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=pw_hash, birthday = request.POST["birthday"], gender=request.POST["gender"], city = request.POST["city"])

        request.session['user_id'] = user.id
        request.session['user_first'] = user.first_name
        return redirect('/')


def process_login(request):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if not EMAIL_REGEX.match(request.POST['login_email']): 
        errors["login_email"] = "Please enter an email address"

    if len(request.POST['login_password']) < 1:
        errors["login_password"] = "Please enter a password"

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/login/')
    
    user = User.objects.filter(email=request.POST['login_email'])
    if user:
        print("there is a user")
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
            request.session["user_id"] = logged_user.id
            request.session["user_first"] = logged_user.first_name
            return redirect('/')
        else:
            messages.error(request, "Incorrect password")
            return redirect("/login/")
    else:
        messages.error(request,"User does not exist")
    return redirect("/login/")
def display_login(request):
    return render(request, 'login.html')
def display_message(request):
    return render(request, 'message.html')
def display_profile(request):
    return render(request, 'profile.html')

def display_game(request):
    random_id = random.randint(1,44)

    try:
        Game.objects.get(id=random_id)
        question=Game.objects.get(id=random_id)
        print("used try")
    except:
        random_id = random.randint(22,44)
        question = Game.objects.get(id=random_id)
        print("used except")
    
    logged_user = User.objects.get(id=request.session["user_id"])

    context={
        "question":question,
        "logged_user":logged_user,

    }
    return render(request,'game.html', context)

def process_game(request):
    request.session["answer_id"] = request.POST["option"]

    return redirect('/game/')

