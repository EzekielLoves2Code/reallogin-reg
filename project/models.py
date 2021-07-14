from django.db import models
from datetime import datetime
import re


class userManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['first_name']) < 3:
            errors['first_name'] = "first name should be at least 3 characters"
        if len(form['last_name']) < 3:
            errors['last_name'] = "Last name should at least be 3 characters"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = ("Invalid email address!")
        if len(form['password']) < 8:
            errors['password'] = "password must be at least 8 characters"
        if form['password'] != form['confpass']:
            errors['password'] = "Passswords do not match!"
        return errors


class IdeaManager(models.Manager):
    def ideavalidator(self, postData):
        errors = {}
        print(postData)
        if len(postData['name']) < 3:
            errors['name'] = "Idea Name should at least be 3 characters"
        if len(postData['description']) < 3:
            errors['description'] = "Description should be at least 3 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=35)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)
    objects = userManager()


class Idea(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=55)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)
    objects = IdeaManager()

    uploaded_by = models.ForeignKey(
        User, related_name="ideas_uploaded", on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
