# Generated by Django 5.1.4 on 2024-12-24 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='is_admin',
            new_name='is_librarian',
        ),
    ]
