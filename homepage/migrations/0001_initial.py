# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('duoshuo_id', models.IntegerField(default=0)),
                ('token', models.IntegerField(default=0)),
                ('avatar', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
        ),
    ]
