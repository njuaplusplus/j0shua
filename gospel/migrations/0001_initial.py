# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u59d3\u540d')),
                ('email', models.EmailField(max_length=254, verbose_name='\u90ae\u4ef6')),
                ('phone', models.CharField(max_length=255, verbose_name='\u7535\u8bdd')),
                ('message', models.TextField(verbose_name='\u4fe1\u606f')),
                ('date_created', models.DateTimeField(verbose_name='\u7559\u8a00\u65e5\u671f')),
            ],
            options={
                'ordering': ['-date_created'],
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
    ]
