# Generated by Django 5.0.4 on 2024-04-27 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_profile.png', null=True, upload_to='profiles'),
        ),
    ]
