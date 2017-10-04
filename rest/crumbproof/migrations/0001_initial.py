# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 06:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField()),
                ('started', models.DateField()),
                ('completed', models.DateField()),
                ('oven_start', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('content', models.CharField(max_length=256)),
                ('unit', models.CharField(max_length=256)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created', models.DateField()),
                ('updated', models.DateField()),
                ('deleted', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.IntegerField()),
                ('content', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('prep_time', models.IntegerField()),
                ('bake_time', models.IntegerField()),
                ('yield_count', models.IntegerField()),
                ('yield_type', models.CharField(max_length=256)),
                ('created', models.DateField()),
                ('updated', models.DateField()),
                ('deleted', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='instruction',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crumbproof.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crumbproof.Recipe'),
        ),
        migrations.AddField(
            model_name='activity',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crumbproof.Recipe'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
