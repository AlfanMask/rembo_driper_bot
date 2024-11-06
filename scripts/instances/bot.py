from dotenv import load_dotenv
from aiogram import Bot
from aiogram.enums import ParseMode

# load all env variables
load_dotenv()
import os

# get env variables
api_key = os.getenv("API_TOKEN")
bot = Bot(token=api_key, parse_mode=ParseMode.MARKDOWN)