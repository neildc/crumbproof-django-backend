# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-18 05:23
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crumbproof', '0002_scheduledpushnotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityInProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_step', models.IntegerField(default=0)),
                ('start_times', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('end_times', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crumbproof.Recipe')),
            ],
        ),
        migrations.RenameField(
            model_name='scheduledpushnotification',
            old_name='payload',
            new_name='data',
        ),
        migrations.RemoveField(
            model_name='scheduledpushnotification',
            name='title',
        ),
        migrations.RemoveField(
            model_name='scheduledpushnotification',
            name='token',
        ),
        migrations.RemoveField(
            model_name='scheduledpushnotification',
            name='topic',
        ),
        migrations.AddField(
            model_name='scheduledpushnotification',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_push_notifications', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='push_subscription',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='activityinprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_in_progress', to=settings.AUTH_USER_MODEL),
        ),
    ]
