# Generated by Django 3.1.1 on 2020-10-05 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses_site', '0005_video_order_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='order_number',
        ),
    ]
