from dotenv import load_dotenv
import os
import asyncio
import django
from django.conf import settings
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta
from django.core.files.storage import default_storage

# Load the .env file
load_dotenv()

# Get the API key and channel ID from environment variables
telegram_api_key = os.getenv('TELEGRAM_API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techsync.settings')

# Initialize Django
django.setup()

# Import Django models after setup
from projects.models import Project

# Initialize the Telegram Bot
bot = Bot(token=telegram_api_key)

async def fetch_best_project_daily():
    """
    Fetches the best project based on vote_count for the daily period.
    """
    now = datetime.now()
    start_time = now - timedelta(days=1)
    print(f"Fetching projects created after: {start_time}")
    return await sync_to_async(lambda: Project.objects.filter(created_at__gte=start_time).order_by('-vote_count').first())()

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

async def test_daily_post_logic():
    """
    Tests the logic for posting the best daily project to the Telegram channel.
    """
    try:
        project = await fetch_best_project_daily()
        if project:
            print(f"Best project for the day: {project.title}")
            owner = await sync_to_async(lambda: project.owner.name or project.owner.username)()
            description = (project.description[:200] + '...') if project.description else 'No description available.'
            view_more_link = f"http://127.0.0.1:8000/projects/project_detail/{project.id}/"
            
            message = (
                f"<b>{project.title}</b>\n\n"
                f"Owner: {owner}\n\n"
                f"{description}\n\n"
                f"<a href='{view_more_link}'>View More</a>"
            )

            # Check if there is an image to include in the post
            if project.image:
                # Adjust the path to the image file
                image_path = project.image.path
                print(f"Image path: {image_path}")

                if os.path.exists(image_path):
                    with open(image_path, 'rb') as photo_file:
                        await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_file, caption=message, parse_mode=ParseMode.HTML)
                        print("Image sent successfully!")
                else:
                    print(f"Image file not found: {image_path}")
            else:
                # No image to include in the post
                await send_message_to_channel(message, photo_url=None)

        else:
            print("No projects found for the daily period.")
    except Exception as e:
        print(f"Error fetching or sending project: {e}")

if __name__ == '__main__':
    asyncio.run(test_daily_post_logic())
