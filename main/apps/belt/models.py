# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "User name must be more than two characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter in a valid email address!"
        if len(postData['password']) != len(postData['cpassword']):
            errors['password'] = "Passwords must match!"
        return errors
    # def login(self, postData):
    #     errors1 = {}
    #     if (len(postData['email']) or len(postData['password'])) < 1:
    #         errors1['field_empty'] = "Fields can not be empty!"
    #     user_list = []
    #     user_list = User.objects.filter(email = postData['email'])
    #     if (user_list):
    #         login_pass = postData['password']
    #         check = bcrypt.checkpw(login_pass.encode(),user_list[0].password.encode())
    #         if(check is False):
    #             errors1['wrong'] = "Wrong Username or Password!"
    #     else:
    #         errors1['wrong'] = "Wrong Username or Password!"
    #     return errors1

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    cpassword = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return self.name, self.email

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return self.title, self.author

class Review(models.Model):
    review = models.CharField(max_length=255)
    rating = models.IntegerField(default=3)
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
