import logging, datetime
from helper import gemini
from constants import peak_hours
from instances.client import client

async def worker() -> None:
    try:
        # give motivation on drivers group each peak hours
        for peak_hour in peak_hours.ph_list.values():
            start_time = datetime.datetime.combine(datetime.datetime.today(), peak_hour)
            end_time = start_time + datetime.timedelta(minutes=10)
            if is_now_between(start_time, end_time):
                await gemini.send_motivation(peak_hour)
                return #stop the function so not giving multiple motivation as below

        # checking if there is many orders don't get drivers -> announce to drivers group
        is_many_orders_dont_get_driver = client.magers.get.is_many_orders_dont_get_driver()
        if is_many_orders_dont_get_driver:
            await gemini.announce_many_orders_dont_get_driver()
        
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