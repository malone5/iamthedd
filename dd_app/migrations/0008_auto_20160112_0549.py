# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-12 10:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dd_app', '0007_auto_20160112_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crew',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 12, 10, 49, 45, 323629, tzinfo=utc), verbose_name='date created'),
        ),
    ]