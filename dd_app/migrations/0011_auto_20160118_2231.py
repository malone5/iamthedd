# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 03:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dd_app', '0010_auto_20160113_0018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crewmember',
            old_name='crew_name',
            new_name='crew',
        ),
        migrations.AlterField(
            model_name='crew',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 3, 30, 46, 189593, tzinfo=utc), verbose_name='date created'),
        ),
    ]
