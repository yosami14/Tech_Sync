# Generated by Django 5.0.4 on 2024-07-03 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_remove_eventmoderator_moderation_history_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmoderator',
            name='permissions',
        ),
    ]
