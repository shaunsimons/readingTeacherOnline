# Generated by Django 3.1.1 on 2020-11-20 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_site', '0012_auto_20201118_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='length',
            field=models.DurationField(),
        ),
    ]
