# Generated by Django 5.1.4 on 2024-12-29 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_alter_profile_hostel_alter_profile_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='hostel',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='room',
        ),
    ]
