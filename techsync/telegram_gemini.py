import os
import re
import requests
import logging
from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
GEMINI_API_URL = 'http://127.0.0.1:8000/chatbot/telegram-to-gemini/'  # Your Django endpoint

# Initialize the Telegram Bot
bot = Bot(token=TELEGRAM_API_KEY)

def escape_markdown_v2(text):
    """Escapes characters for Markdown V2."""
    # Markdown V2 reserved characters
    return re.sub(r'([_*\[\]()~`>#+-=|{}.!])', r'\\\1', text)

async def start(update: Update, context: CallbackContext):
    start_message = (
        "Welcome to Techsync Bot! 🤖\n\n"
        "I'm here to help you with information about Techsync projects and events.\n\n"
        "To get started, just type your message and I'll assist you with any questions or information you need.\n"
        "Feel free to ask me about project details, event announcements, or anything else related to Techsync."
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
                # Escape special characters for Markdown V2
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

def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()
