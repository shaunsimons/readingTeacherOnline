# Generated by Django 3.1.1 on 2021-01-25 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210104_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutme',
            name='description',
            field=models.TextField(),
        ),
    ]
