# Generated by Django 5.1.4 on 2024-12-29 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_feedback_feedbackimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='content',
            field=models.TextField(max_length=250),
        ),
    ]
