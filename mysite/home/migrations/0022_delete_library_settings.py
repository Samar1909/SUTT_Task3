# Generated by Django 5.1.4 on 2024-12-26 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_remove_returnbook_book_remove_returnbook_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='library_settings',
        ),
    ]
