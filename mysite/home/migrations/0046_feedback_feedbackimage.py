# Generated by Django 5.1.4 on 2024-12-29 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0045_remove_feedback_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='feedbackImage',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='feedbackImage'),
        ),
    ]
