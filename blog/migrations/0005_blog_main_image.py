# Generated by Django 3.1.1 on 2020-09-12 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_blog_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='main_image',
            field=models.ImageField(default='blog/images/readingwithkids.jpg             ', upload_to='blog/images'),
        ),
    ]
