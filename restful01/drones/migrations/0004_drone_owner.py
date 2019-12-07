# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-12-07 14:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drones', '0003_auto_20191206_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='drone',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='drones', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
