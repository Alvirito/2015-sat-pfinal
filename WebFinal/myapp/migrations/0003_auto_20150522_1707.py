# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_personal'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='fondo',
            field=models.TextField(default=0, max_length=9999),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personal',
            name='letra',
            field=models.TextField(default=0, max_length=9999),
            preserve_default=False,
        ),
    ]
