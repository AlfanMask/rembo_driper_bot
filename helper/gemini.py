import logging, datetime
from dotenv import load_dotenv
# load all env variables
load_dotenv()
import os
from scripts.instances.bot import bot
from scripts.instances.gemini_ai import model
from constants import prompts
# setup gemini ai instance
group_chat_id = os.getenv("GROUP_CHAT_ID")

async def send_motivation():
    try:
        response = model.generate_content(prompts.active_driver_motivation)
        await bot.send_message(
            chat_id=group_chat_id,
            text=response.text,
            parse_mode="Markdown",
            request_timeout=300,
        )
    except Exception as e:
        print(f"error: {e}")
        logging.error(f"{datetime.datetime.now()} - Error: {e}")