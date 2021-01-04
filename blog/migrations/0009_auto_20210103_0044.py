# Generated by Django 3.1.1 on 2021-01-03 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_aboutme'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.FileField(default=None, null=True, upload_to=''),
        ),
    ]