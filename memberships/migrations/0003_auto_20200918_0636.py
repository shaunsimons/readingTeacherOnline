# Generated by Django 3.1.1 on 2020-09-18 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0002_coupons'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='stripid',
            new_name='stripeid',
        ),
    ]
