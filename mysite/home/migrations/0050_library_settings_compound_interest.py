# Generated by Django 5.1.4 on 2025-01-21 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_favourite'),
    ]

    operations = [
        migrations.AddField(
            model_name='library_settings',
            name='compound_interest',
            field=models.IntegerField(default=0),
        ),
    ]
