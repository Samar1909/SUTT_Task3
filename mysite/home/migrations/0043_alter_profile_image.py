# Generated by Django 5.1.4 on 2024-12-29 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_auto_20241229_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_placeholder.jpg', upload_to='profile_pics'),
        ),
    ]
