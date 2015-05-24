# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activitie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Identificador', models.TextField(max_length=9999)),
                ('name', models.TextField(max_length=9999)),
                ('price', models.TextField(max_length=9999)),
                ('date', models.TextField(max_length=9999)),
                ('startHour', models.TextField(max_length=9999)),
                ('typ', models.TextField(max_length=9999)),
                ('timeToLong', models.TextField(max_length=9999)),
                ('Long', models.TextField(max_length=9999)),
                ('Url', models.TextField(max_length=9999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='elegidas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.TextField(max_length=9999)),
                ('Identificador', models.TextField(max_length=9999)),
                ('name', models.TextField(max_length=9999)),
                ('price', models.TextField(max_length=9999)),
                ('date', models.TextField(max_length=9999)),
                ('startHour', models.TextField(max_length=9999)),
                ('typ', models.TextField(max_length=9999)),
                ('timeToLong', models.TextField(max_length=9999)),
                ('Long', models.TextField(max_length=9999)),
                ('Url', models.TextField(max_length=9999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=9999)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
