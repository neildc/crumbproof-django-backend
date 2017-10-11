from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=256)
    prep_time = models.IntegerField()
    bake_time = models.IntegerField()
    oven_temperature = models.IntegerField()
    yield_count = models.IntegerField()
    yield_type = models.CharField(max_length=256)
    user_id = models.ForeignKey(User)
    live = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)


class Activity(models.Model):
    user_id = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    recipe_id = models.ForeignKey( Recipe
                                 , related_name='activities'
                                 , on_delete=models.CASCADE
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

class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    recipe_id = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    unit = models.CharField(max_length=256)
    quantity = models.DecimalField(decimal_places=2, max_digits=5)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

class Instruction(models.Model):
    recipe_id = models.ForeignKey(Recipe, related_name='instructions', on_delete=models.CASCADE)
    step_number = models.IntegerField()
    content = models.CharField(max_length=1024)
    time_gap_to_next = models.IntegerField(null=True)
