# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 06:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dd_app', '0017_auto_20160125_0340'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='venue',
            field=models.CharField(choices=[(b'Bar', b'Bar'), (b'Club', b'Club'), (b'HouseParty', b'HouseParty')], default='Bar', max_length=20),
        ),
        migrations.AlterField(
            model_name='crew',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 26, 6, 50, 40, 195554, tzinfo=utc), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='crewmember',
            name='personality',
            field=models.CharField(choices=[(b'Bar', b'Bar'), (b'Club', b'Club'), (b'HouseParty', b'HouseParty')], default='Angry', max_length=20),
        ),
    ]
