# Generated by Django 5.0.4 on 2024-07-03 13:12

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0012_alter_chatgroup_group_name_alter_groupmessage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=100, unique=True),
        ),
    ]
