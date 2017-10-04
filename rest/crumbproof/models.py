from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=256)
    prep_time = models.IntegerField()
    bake_time = models.IntegerField()
    yield_count = models.IntegerField()
    yield_type = models.CharField(max_length=256)
    user_id = models.ForeignKey(User)
    created = models.DateField()
    updated = models.DateField()
    deleted = models.DateField()


class Activity(models.Model):
    user_id = models.ForeignKey(User)
    recipe_id = models.ForeignKey(Recipe)
    created = models.DateField()
    started = models.DateField()
    completed = models.DateField()
    oven_start = models.DateField()

class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    recipe_id = models.ForeignKey(Recipe)
    content = models.CharField(max_length=256)
    unit = models.CharField(max_length=256)
    quantity = models.DecimalField(decimal_places=2, max_digits=5)
    created = models.DateField()
    updated = models.DateField()
    deleted = models.DateField()

class Instruction(models.Model):
    recipe_id = models.ForeignKey(Recipe)
    step_number = models.IntegerField()
    content = models.CharField(max_length=256)
