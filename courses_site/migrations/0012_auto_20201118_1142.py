# Generated by Django 3.1.1 on 2020-11-18 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_site', '0011_video_activity_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='video',
            name='length',
            field=models.DurationField(editable=False),
        ),
    ]
