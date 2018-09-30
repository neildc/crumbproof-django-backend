# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 04:26
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crumbproof', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledPushNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('launch_time', models.DateTimeField()),
                ('title', models.CharField(max_length=256)),
                ('topic', models.CharField(max_length=256)),
                ('token', models.CharField(max_length=256)),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]