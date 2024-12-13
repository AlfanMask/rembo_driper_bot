import logging, datetime
from helper import gemini
from constants import peak_hours, univs
from instances.client import client

# For ticking check alraedy more then 1H
# for many orders dont get drivers so bot can announce to the group, but only once per hour (6 times of worker run. each worker run = 10 minutes)
global ticking_number_worker_run
ticking_number_worker_run: int = 0
global is_sent_motivation_is_many_orders_dont_get_driver
is_sent_motivation_is_many_orders_dont_get_driver: bool = False

# worker will run every 10 minutes
async def worker() -> None:
    try:
        global ticking_number_worker_run
        global is_sent_motivation_is_many_orders_dont_get_driver
        
        # give motivation on drivers group each peak hours
        for peak_hour in peak_hours.ph_list.values():
            start_time = datetime.datetime.combine(datetime.datetime.today(), peak_hour)
            end_time = start_time + datetime.timedelta(minutes=10)
            if is_now_between(start_time, end_time):
                await gemini.send_motivation(peak_hour)
                return #stop the function so not giving multiple motivation as below

        # for UNS campus
        (anjem_uns_dont_get_drivers_link, order_msg) = client.magers.get.newest_anjem_uns_dont_get_drivers_link()
        if anjem_uns_dont_get_drivers_link:
            await gemini.announce_anjem_dont_get_driver(anjem_uns_dont_get_drivers_link, order_msg, univs.uns)
            client.magers.update.set_is_reminded_true_by_link(anjem_uns_dont_get_drivers_link)
            
        # for UMS campus
        (anjem_ums_dont_get_drivers_link, order_msg) = client.magers.get.newest_anjem_ums_dont_get_drivers_link()
        if anjem_ums_dont_get_drivers_link:
            await gemini.announce_anjem_dont_get_driver(anjem_ums_dont_get_drivers_link, order_msg, univs.ums)
            client.magers.update.set_is_reminded_true_by_link(anjem_ums_dont_get_drivers_link)

        # checking if there is many orders don't get drivers -> announce to drivers group
        # FOR NOW: only for uns
        is_many_orders_dont_get_driver = client.magers.get.is_many_orders_dont_get_driver()
        if is_many_orders_dont_get_driver and not is_sent_motivation_is_many_orders_dont_get_driver:
            await gemini.announce_many_orders_dont_get_driver()
            is_sent_motivation_is_many_orders_dont_get_driver = True
            ticking_number_worker_run = 0
            return
        
        # count how many times the worker run
        # if more then 6 times -> reset value of is_sent_motivation_is_many_orders_dont_get_driver so then able to send another motivation after already 1H
        if ticking_number_worker_run < 6:
            ticking_number_worker_run += 1
        else:
            is_sent_motivation_is_many_orders_dont_get_driver = False
            ticking_number_worker_run = 0
        
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