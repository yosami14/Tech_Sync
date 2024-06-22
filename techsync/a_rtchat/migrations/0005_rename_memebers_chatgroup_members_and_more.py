# Generated by Django 5.0.4 on 2024-06-22 07:52

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0004_alter_chatgroup_group_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatgroup',
            old_name='memebers',
            new_name='members',
        ),
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=100, unique=True),
        ),
    ]
