import pandas as pd
from django.core.management.base import BaseCommand
from projects.models import Project
from event.models import Event  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Export Project and Event data to Excel'

    def handle(self, *args, **kwargs):
        # Export Project data
        project_data = Project.objects.select_related('owner__user').all().values(
            'id',
            'title',
            'description',
            'demo_link',
            'source_link',
            'owner__id',  # Profile ID
            'owner__name',  # Profile name
            'owner__user__email'  # User email
        )

        # Add 'more_information' column for Project
        project_df = pd.DataFrame(project_data)
        project_df['more_information'] = 'http://127.0.0.1:8000/projects/project_detail/' + project_df['id'].astype(str)

        # Export Event data
        event_data = Event.objects.select_related('organizer').all().values(
            'id',
            'title',
            'description',
            'date',
            'end_date',
            'location_type',
            'location',
            'venue_name',
            'place',
            'organizer__id',  # EventOrganizer ID
            'organizer__name'  # EventOrganizer name
        )

        # Convert datetime fields to naive (remove timezone information)
        event_df = pd.DataFrame(event_data)
        if not event_df.empty:
            for col in ['date', 'end_date', 'created_at', 'updated_at']:
                if col in event_df.columns:
                    event_df[col] = pd.to_datetime(event_df[col]).dt.tz_localize(None)

        # Add 'more_information' column for Event
        event_df['more_information'] = 'http://127.0.0.1:8000/event/event_detail/' + event_df['id'].astype(str)

        # Write to Excel
        with pd.ExcelWriter('data_export.xlsx', engine='openpyxl') as writer:
            project_df.to_excel(writer, sheet_name='Projects', index=False)
            event_df.to_excel(writer, sheet_name='Events', index=False)

        self.stdout.write(self.style.SUCCESS('Successfully exported Project and Event data to Excel'))
