from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField


class Recipe(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    data = JSONField();
    diff = JSONField(null=True);
    base_recipe = models.ForeignKey('self', related_name='variations', null=True)
    parent = models.ForeignKey('self', null=True)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True)


class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='activities',
                             on_delete=models.CASCADE)

    recipe = models.ForeignKey( Recipe
                                 , related_name='activities'
                                 , null=True
                                 )
    name = models.CharField(max_length=256)
    crumb_shot = models.ImageField(upload_to='images', max_length=None)
    created = models.DateTimeField(auto_now_add=True)
    started = models.DateTimeField(null=True)
    completed = models.DateTimeField(null=True)
    oven_start = models.DateTimeField(null=True)
    oven_end = models.DateTimeField(null=True)
    notes = models.CharField(max_length=3000, null=True)

class User(AbstractUser):
    favourite_recipes = models.ManyToManyField(Recipe, related_name='favorited_by')
