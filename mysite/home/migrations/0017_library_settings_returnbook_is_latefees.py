# Generated by Django 5.1.4 on 2024-12-26 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_returnbook'),
    ]

    operations = [
        migrations.CreateModel(
            name='library_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('late_fees', models.IntegerField()),
                ('issue_period', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='returnbook',
            name='is_latefees',
            field=models.BooleanField(default=False),
        ),
    ]