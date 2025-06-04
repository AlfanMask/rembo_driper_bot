import logging, datetime
from helper import gemini, weather
from constants import peak_hours, univs
from instances.client import client

# For ticking check alraedy more then 1H
# for many orders dont get drivers so bot can announce to the group, but only once per hour (6 times of worker run. each worker run = 10 minutes)
global ticking_number_worker_run_motivation_dont_get_drivers
ticking_number_worker_run_motivation_dont_get_drivers: int = 0
global is_sent_motivation_is_many_orders_dont_get_driver
is_sent_motivation_is_many_orders_dont_get_driver: bool = False

# for announcing will rain
global ticking_number_worker_run_announce_will_rain
ticking_number_worker_run_announce_will_rain: int = 0
global is_sent_will_rain
is_sent_will_rain: bool = False

# worker will run every 10 minutes
async def worker() -> None:
    try:
        global ticking_number_worker_run_motivation_dont_get_drivers
        global is_sent_motivation_is_many_orders_dont_get_driver
        global ticking_number_worker_run_announce_will_rain
        global is_sent_will_rain
        
        # give motivation on drivers group each peak hours
        for peak_hour in peak_hours.ph_list.values():
            start_time = datetime.datetime.combine(datetime.datetime.today(), peak_hour)
            end_time = start_time + datetime.timedelta(minutes=5)
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
            
        # for UNY campus
        (anjem_uny_dont_get_drivers_link, order_msg) = client.magers.get.newest_anjem_uny_dont_get_drivers_link()
        if anjem_uny_dont_get_drivers_link:
            await gemini.announce_anjem_dont_get_driver(anjem_uny_dont_get_drivers_link, order_msg, univs.uny)
            client.magers.update.set_is_reminded_true_by_link(anjem_uny_dont_get_drivers_link)

        # checking if there is many orders don't get drivers -> announce to drivers group
        # FOR NOW: only for uns
        is_many_orders_dont_get_driver = client.magers.get.is_many_orders_dont_get_driver()
        if is_many_orders_dont_get_driver and not is_sent_motivation_is_many_orders_dont_get_driver:
            await gemini.announce_many_orders_dont_get_driver()
            is_sent_motivation_is_many_orders_dont_get_driver = True
            ticking_number_worker_run_motivation_dont_get_drivers = 0
            return
        
        # check if will rain -> anounce to drivers group
        # FOR NOW: only for uns
        (cuaca_result_now, cuaca_result_future) = await weather.get_weather_by_univ(univs.uns)
        if "hujan" in cuaca_result_future.lower() and not is_sent_will_rain:
            await gemini.announce_will_rain(univs.uns, cuaca_result_future)
            is_sent_will_rain = True
            ticking_number_worker_run_announce_will_rain = 0
        
        # count how many times the worker run
        # if more then 6 times -> reset value of is_sent_motivation_is_many_orders_dont_get_driver so then able to send another motivation after already 1H
        if ticking_number_worker_run_motivation_dont_get_drivers < 12:
            ticking_number_worker_run_motivation_dont_get_drivers += 1
        else:
            is_sent_motivation_is_many_orders_dont_get_driver = False
            ticking_number_worker_run_motivation_dont_get_drivers = 0

        # if more then 18 times -> reset value of is_sent_motivation_is_many_orders_dont_get_driver so then able to send another motivation after already 3H (like on interval on BMKG data terbuka weather forecasting)
        if ticking_number_worker_run_announce_will_rain < 36:
            ticking_number_worker_run_announce_will_rain += 1
        else:
            is_sent_will_rain = False
            ticking_number_worker_run_announce_will_rain = 0 
        
    except Exception as e:
        print(f"worker error: {e}")
        logging.error(f"{datetime.datetime.now()} - worker Error: {e}")
        
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