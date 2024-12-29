from django.db import migrations

def update_default_image(apps, schema_editor):
    Profile = apps.get_model('home', 'Profile')
    new_url = 'profile_pics/profile_placeholder.jpg'  # Replace with your old default URL
    old_url = 'profile_placeholder.jpg'  # Replace with your new default URL

    Profile.objects.filter(image=old_url).update(image=new_url)

class Migration(migrations.Migration):
    dependencies = [
        ('home', '0040_alter_profile_image'),
    ]

    operations = [
        migrations.RunPython(update_default_image),
    ]