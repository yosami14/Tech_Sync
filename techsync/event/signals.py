import os
import asyncio
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from .models import Event
from django.conf import settings  # Use Django settings for API keys

CHANNEL_ID = -1002445584860
TELEGRAM_API_KEY = '7073386598:AAGsPT4QHgarUbux-BjzmjotjBMo3TeeoPg'
BOT_USERNAME = 'techsyncs_bot'  
bot = Bot(token=TELEGRAM_API_KEY)

MAX_CAPTION_LENGTH = 1024  # Telegram's maximum length for a message caption

@receiver(post_save, sender=Event)
def event_post_save(sender, instance, **kwargs):
    """
    Signal receiver that sends a message to the Telegram channel when an event is created or updated.
    """
    created = kwargs.get('created', False)
    
    # Handle both creation and updates
    event = instance

    # Create a shorter message with a truncated description and clear links
    description = event.description.replace('<p>', '').replace('</p>', '')  # Remove unsupported <p> tags
    if len(description) > 200:  # Limit description to 200 characters
        description = description[:197] + '...'  # Truncate and add ellipsis

    message = (
        "<b>{}</b>\n"
        "Date: {}\n\n"
        "{}\n\n"
        "<a href='http://127.0.0.1:8000/event/event_detail/{}/'>View More</a>\n"
        "<a href='tg://resolve?domain={}&start=register_event_{}'>Register</a>"
    ).format(
        event.title,
        event.date,
        description,  # Shortened description
        event.id,  # For "View More" link
        BOT_USERNAME,  # For "Register" deep link
        event.id  # Pass event ID to the bot
    )

    # Ensure message is within Telegram's caption length limit
    if len(message) > MAX_CAPTION_LENGTH:
        message = message[:MAX_CAPTION_LENGTH - 3] + '...'  # Truncate and add ellipsis

    async def send_message():
        try:
            if event.event_image:
                # Get the full path to the image file
                image_path = event.event_image.path
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as photo_file:
                        await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_file, caption=message, parse_mode=ParseMode.HTML)
                        print("Image sent successfully!")
                else:
                    print(f"Image file not found: {image_path}")
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)
            else:
                # No image to include in the post
                await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)
                print("Message sent successfully without image!")
        except TelegramError as e:
            print(f"Failed to send message: {e}")

    # Run the async function in a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message())
    loop.close()
