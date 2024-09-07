import os
import re
import requests
import logging
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    filters,
)
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
GEMINI_API_URL = 'http://127.0.0.1:8000/chatbot/telegram-to-gemini/'  # Your Django endpoint
DJANGO_REGISTER_URL = 'http://127.0.0.1:8000/chatbot/register/'  # Update with your Django API URL

# Initialize the Telegram Bot
bot = Bot(token=TELEGRAM_API_KEY)

# States for the registration flow
FIRST_NAME, USERNAME, EMAIL, PASSWORD = range(4)


def escape_markdown_v2(text):
    """Escapes characters for Markdown V2."""
    return re.sub(r'([_*\[\]()~`>#+-=|{}.!])', r'\\\1', text)


async def start(update: Update, context: CallbackContext):
    start_message = (
        "Welcome to Techsync Bot! 🤖\n\n"
        "I'm here to help you with information about Techsync projects and events.\n\n"
        "Type /register to create a new account or just type a message to chat with me."
    )
    await update.message.reply_text(start_message)


async def handle_message(update: Update, context: CallbackContext):
    if update.message:
        user_message = update.message.text
        logger.info(f"Received message: {user_message}")
        try:
            response = requests.post(
                GEMINI_API_URL,
                data={'message': user_message}  # Sending data as form-urlencoded
            )

            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content: {response.content}")

            if response.status_code == 200:
                data = response.json()
                gemini_response = data.get('response', 'No response key in JSON')
                escaped_response = escape_markdown_v2(gemini_response)
                await update.message.reply_text(
                    escaped_response,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            else:
                await update.message.reply_text("Sorry, I encountered an error.")
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            await update.message.reply_text("Sorry, I encountered an error.")
    else:
        logger.warning("Received an update without a message.")


async def register(update: Update, context: CallbackContext):
    await update.message.reply_text("Please provide your first name:")
    return FIRST_NAME


async def first_name(update: Update, context: CallbackContext):
    context.user_data['first_name'] = update.message.text
    await update.message.reply_text("Please provide your username:")
    return USERNAME


async def username(update: Update, context: CallbackContext):
    context.user_data['username'] = update.message.text
    await update.message.reply_text("Please provide your email:")
    return EMAIL


async def email(update: Update, context: CallbackContext):
    context.user_data['email'] = update.message.text
    await update.message.reply_text("Please provide your password:")
    return PASSWORD


async def password(update: Update, context: CallbackContext):
    context.user_data['password'] = update.message.text

    # Send registration data to Django API
    user_data = {
        'first_name': context.user_data['first_name'],
        'username': context.user_data['username'],
        'email': context.user_data['email'],
        'password1': context.user_data['password'],
        'password2': context.user_data['password'],
    }

    response = requests.post(DJANGO_REGISTER_URL, json=user_data)
    if response.status_code == 201:
        await update.message.reply_text("Registration successful! Welcome to our platform.")
    else:
        errors = response.json().get('errors', 'An error occurred.')
        await update.message.reply_text(f"Registration failed: {errors}")

    return ConversationHandler.END


def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Registration Conversation Handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("register", register)],
        states={
            FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_name)],
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, username)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
