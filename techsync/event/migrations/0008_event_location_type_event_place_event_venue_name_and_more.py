# Generated by Django 5.0.4 on 2024-07-10 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_alter_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location_type',
            field=models.CharField(choices=[('VENUE', 'Venue'), ('ONLINE', 'Online')], default='VENUE', max_length=6),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='venue_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
