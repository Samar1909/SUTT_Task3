# Generated by Django 5.1.4 on 2024-12-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_alter_feedback_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='content',
            field=models.TextField(),
        ),
    ]
