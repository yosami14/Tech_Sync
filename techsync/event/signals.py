import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from .models import Event
import asyncio

CHANNEL_ID = -1002445584860
TELEGRAM_API_KEY = '7073386598:AAGsPT4QHgarUbux-BjzmjotjBMo3TeeoPg'

# Initialize the Telegram Bot
bot = Bot(token=TELEGRAM_API_KEY)
print("Telegram API Key:", TELEGRAM_API_KEY)

@receiver(post_save, sender=Event)
def event_post_save(sender, instance, **kwargs):
    """
    Signal receiver that sends a message to the Telegram channel when an event is created or updated.
    """
    created = kwargs.get('created', False)
    
    if created or not created:  # This covers both creation and updates
        print(f"Signal triggered for event ID: {instance.id}")
        event = instance

        # Compose the message
        message = (
            "<b>{}</b>\n\n"
            "Date: {}\n\n"
            "Description: {}\n\n"
            "{}{}"
            "<a href='http://127.0.0.1:8000/events/{}/'>View More</a>"
        ).format(
            event.title,
            event.date,
            event.description.replace('<p>', '').replace('</p>', ''),  # Remove unsupported <p> tags
            'Location: {}\n'.format(event.location) if event.location else '',
            'Venue: {}\n'.format(event.venue_name) if event.venue_name else '',
            event.id
        )

        # Check if there is an image to include in the post
        if event.event_image:
            # Get the full path to the image file
            image_path = event.event_image.path
            print(f"Image path: {image_path}")

            async def send_message():
                try:
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as photo_file:
                            await bot.send_photo(chat_id=CHANNEL_ID, photo=photo_file, caption=message, parse_mode=ParseMode.HTML)
                            print("Image sent successfully!")
                    else:
                        print(f"Image file not found: {image_path}")
                        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)
                except TelegramError as e:
                    print(f"Failed to send message: {e}")

            # Run the async function
            asyncio.run(send_message())
        else:
            # No image to include in the post
            async def send_message_without_image():
                try:
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)
                    print("Message sent successfully without image!")
                except TelegramError as e:
                    print(f"Failed to send message: {e}")

            # Run the async function
            asyncio.run(send_message_without_image())
    else:
        print("Signal not triggered: neither created nor update_fields")
