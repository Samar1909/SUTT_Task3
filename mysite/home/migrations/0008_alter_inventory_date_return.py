# Generated by Django 5.1.4 on 2024-12-25 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_inventory_date_return'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='date_return',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
