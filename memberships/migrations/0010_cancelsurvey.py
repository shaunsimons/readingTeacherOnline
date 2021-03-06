# Generated by Django 3.1.1 on 2020-09-25 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0009_auto_20200925_0552'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satisfaction', models.IntegerField(choices=[(0, 'Very Satisfied'), (1, 'Satisfied'), (2, 'Neutral'), (3, 'Unsatisfied'), (4, 'Very Unsatisfied')])),
                ('primary_reason', models.IntegerField()),
                ('other', models.TextField(null=True)),
                ('suggestion', models.TextField(null=True)),
            ],
        ),
    ]
