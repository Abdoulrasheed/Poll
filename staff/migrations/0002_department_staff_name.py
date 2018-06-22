# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-21 08:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department_staff',
            name='name',
            field=models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
