# Generated by Django 5.0.4 on 2024-07-03 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_is_event_moderator_user_is_event_organizer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmoderator',
            name='email',
        ),
    ]
