# Generated by Django 3.1.1 on 2020-11-14 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_site', '0008_course_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='length',
            field=models.TimeField(default=datetime.time(0, 1)),
            preserve_default=False,
        ),
    ]
