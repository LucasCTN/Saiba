# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-29 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0013_auto_20170523_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default=b'assets/avatar_default.svg', upload_to=b'avatars/'),
        ),
    ]
