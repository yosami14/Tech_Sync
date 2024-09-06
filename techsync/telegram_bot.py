import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import django
from django.conf import settings
from django.db import models
from django.db.models import Max
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from asgiref.sync import sync_to_async
from django.templatetags.static import static

# Load environment variables
load_dotenv()

# Get the API key and channel ID from environment variables
telegram_api_key = os.getenv('TELEGRAM_API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techsync.settings')
django.setup()

# Import Django models after setup
from projects.models import Project
from users.models import Profile

# Initialize the Telegram Bot
bot = Bot(token=telegram_api_key)

async def fetch_best_project(period):
    """
    Fetches the best project based on vote_count for a given period.
    """
    if period == 'daily':
        time_threshold = datetime.now() - timedelta(days=1)
    elif period == 'weekly':
        time_threshold = datetime.now() - timedelta(weeks=1)
    elif period == 'monthly':
        time_threshold = datetime.now() - timedelta(30)
    else:
        raise ValueError("Invalid period specified")

    # Fetch the best project based on vote_count
    return await sync_to_async(lambda: Project.objects.filter(created_at__gte=time_threshold)
                                       .order_by('-vote_count')
                                       .first())()

async def send_message_to_channel(message, photo_url=None):
    """
    Sends a message to the specified Telegram channel.
    """
    try:
        if photo_url:
            print(f"Sending photo with URL: {photo_url}")
            await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_url, caption=message, parse_mode=ParseMode.HTML)
        else:
            print("Sending text message.")
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)
        print("Message sent successfully!")
    except TelegramError as e:
        print(f"Failed to send message: {e}")

async def post_best_project(period):
    """
    Posts the best project for a given period.
    """
    project = await fetch_best_project(period)
    if project:
        owner = await sync_to_async(lambda: project.owner.name or project.owner.username)()
        description = (project.description[:200] + '...') if project.description else 'No description available.'
        view_more_link = f"http://127.0.0.1:8000/projects/project_detail/{project.id}/"
        
        message = (
            f"<b>{project.title}</b>\n\n"
            f"Owner: {owner}\n\n"
            f"{description}\n\n"
            f"<a href='{view_more_link}'>View More</a>"
        )

        # Generate the absolute URL for the image
        if project.image:
            base_url = 'http://127.0.0.1:8000'
            photo_url = base_url + project.image.url
        else:
            photo_url = None

        print(f"Generated photo URL: {photo_url}")  # Print the URL to check

        await send_message_to_channel(message, photo_url=photo_url)
    else:
        print(f"No projects found for {period}.")

async def schedule_tasks():
    """
    Schedules tasks to post the best project daily, weekly, and monthly.
    """
    while True:
        now = datetime.now()

        # Schedule daily post
        next_daily_run = (now + timedelta(seconds=30)).replace(hour=23, minute=59, second=59, microsecond=0)
        sleep_duration = (next_daily_run - now).total_seconds()
        print(f"Next daily post scheduled in {sleep_duration} seconds.")
        await asyncio.sleep(sleep_duration)
        await post_best_project('daily')

        # Schedule weekly post
        next_weekly_run = (now + timedelta(minutes=1)).replace(hour=23, minute=59, second=59, microsecond=0)
        sleep_duration = (next_weekly_run - now).total_seconds()
        print(f"Next weekly post scheduled in {sleep_duration} seconds.")
        await asyncio.sleep(sleep_duration)
        await post_best_project('weekly')

        # Schedule monthly post
        next_monthly_run = (now + timedelta(minutes=5)).replace(hour=23, minute=59, second=59, microsecond=0)
        sleep_duration = (next_monthly_run - now).total_seconds()
        print(f"Next monthly post scheduled in {sleep_duration} seconds.")
        await asyncio.sleep(sleep_duration)
        await post_best_project('monthly')

if __name__ == '__main__':
    asyncio.run(schedule_tasks())
