# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import User, Book, Review, UserManager
from django.contrib import messages
import bcrypt


# ****************Index Route, Render the Welcome page. This is where you login and register*************************


def index(request):
    return render(request, 'belt/index.html')

# ****************When Registering, Run this Validation**************************************************************

def register(request):
    if request.method == "POST":
        errors = User.objects.validation(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            print "Its working"
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], email=request.POST['email'], password=hash1)
            messages.error(request, 'Registration Successful. Please login in below')
        return redirect('/')

# ****************Login Validation, if valid login info; Redirect to the Home Page*****************************

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    if len(user) == 0:
        messages.error(request, "Invalid Email")
        return redirect('/')
    else:
        if ( bcrypt.checkpw(password.encode(), user[0].password.encode()) ):
            print "Password Matches, Login Successful"
            request.session['id'] = user[0].id
            request.session['email'] = email
            return redirect('/home')
        else:
            messages.error(request, "Invalid Password")
            return redirect('/')        
 
    # if request.method == "POST":
    #     errors1 = User.objects.login(request.POST)
    #     if errors1:
    #         for tag, error in errors1.iteritems():
    #             messages.error(request, error, extra_tags=tag)
    #     print "Right here"
    #     return redirect('/')
    # else:
    #     print "Successful Login"
    #     return redirect('/home')

def home(request):
    context = {
        'users' : User.objects.get(id=request.session['id']),
        'review' : Review.objects.all().order_by('-created_at')[:5],
        'books' : Book.objects.all()
    }
    return render(request, 'belt/home.html', context)
 
def add_book(request):
    return render(request, 'belt/add_book.html')

def create(request):
    if request.POST['select'] != "none":
        r = Book.objects.get(title=request.POST['select'])
        Review.objects.create(review=request.POST['review'], book=Book.objects.get(id=r.id), user=User.objects.get(request.session['email']))
    else:
        r = Book.objects.create(title=request.POST['title'], author=request.POST['author'])
        Review.objects.create(review=request.POST['review'], book=Book.objects.get(id = r.id), user = User.objects.get(email=request.session['email']))
    return redirect('/home')

