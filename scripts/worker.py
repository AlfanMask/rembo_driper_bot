import logging, datetime, schedule
import time
from dotenv import load_dotenv

from constants import numbers, premium_type, prompts
# from instances.db import db
from instances.bot import bot
from instances.gemini_ai import model

# load all env variables
load_dotenv()
import os
# setup gemini ai instance
group_chat_id = os.getenv("GROUP_CHAT_ID")

async def worker() -> None:
    try:
        # TODO: give motivation on drivers group each peak hours (7, 12, 19)
        peak_hours = [datetime.time(10, 0), datetime.time(12, 0), datetime.time(19, 0)]
        for peak_hour in peak_hours:
            start_time = datetime.datetime.combine(datetime.datetime.today(), peak_hour)
            end_time = start_time + datetime.timedelta(hours=1)
            if is_now_between(start_time, end_time):
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
        
# UTILS
def is_now_between(start_time, end_time):
    now = datetime.datetime.now()
    return start_time <= now <= end_time

def is_monday_around_midnight():
    now = datetime.datetime.now()
    if now.weekday() == 0:  # Check if today is Monday
        if now.hour == 0 and 0 <= now.minute <= 5:  # Check if the time is between 0:00 and 0:06
            return True
    return False