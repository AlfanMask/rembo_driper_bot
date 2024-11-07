import logging, datetime
from helper import gemini
# from instances.db import db

async def worker() -> None:
    try:
        # give motivation on drivers group each peak hours (7, 12, 15, 19)
        peak_hours = [datetime.time(6, 30), datetime.time(12, 0), datetime.time(15, 0), datetime.time(19, 0)]
        for peak_hour in peak_hours:
            start_time = datetime.datetime.combine(datetime.datetime.today(), peak_hour)
            end_time = start_time + datetime.timedelta(minutes=10)
            if is_now_between(start_time, end_time):
                await gemini.send_motivation()
        
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