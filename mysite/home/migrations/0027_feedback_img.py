# Generated by Django 5.1.4 on 2024-12-27 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='img',
            field=models.ImageField(default='default.jpg', upload_to='cover_image'),
        ),
    ]
