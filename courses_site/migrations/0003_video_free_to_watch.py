# Generated by Django 3.1.1 on 2020-09-25 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_site', '0002_auto_20200924_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='free_to_watch',
            field=models.BooleanField(default=False),
        ),
    ]
