import os
from dotenv import load_dotenv

load_dotenv()

# Telegram bot token and chat ID from environment variables
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
