
import aiohttp, datetime
from typing import Optional, Tuple
import aiohttp
from constants import kode_lokasi_univ, univs
url: str = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=" # put kode wilayah, check on https://kodewilayah.id/


async def get_weather_by_univ(univ: univs) -> tuple[str, str]:
    try:
        now = datetime.datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}{kode_lokasi_univ.codes[univ]}") as response:
                response_data = await response.json()
                if response.status == 200:
                    cuacas = response_data["data"][0]["cuaca"][0]

                    for i, cuaca in enumerate(cuacas):
                        local_dt = datetime.datetime.fromisoformat(cuaca["local_datetime"])
                        if check_current_cuaca(str(now), str(local_dt)):
                            cuaca_result_now = f"{local_dt.hour:02}-{local_dt.minute:02}: {cuaca['weather_desc']}"
                            
                            # Get next item if available
                            if i < len(cuacas) - 1:
                                next_cuaca = cuacas[i + 1]
                                next_local_dt = datetime.datetime.fromisoformat(next_cuaca["local_datetime"])
                                cuaca_result_future = f"{next_local_dt.hour:02}-{next_local_dt.minute:02}: {next_cuaca['weather_desc']}"
                            else:
                                cuaca_result_future = None
                            
                            return cuaca_result_now, cuaca_result_future

        return None
    except Exception as e:
        print(f"{e}: error getting weather from weather bmkg data terbuka")
        return None
    

async def get_weather_when_stop_rain_by_univ(univ: univs) -> str:
    try:
        now = datetime.datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}{kode_lokasi_univ.codes[univ]}") as response:
                response_data = await response.json()
                if response.status == 200:
                    cuacas = response_data["data"][0]["cuaca"][0]

                    # First, check if it's currently raining
                    current_raining = False
                    current_index = -1
                    
                    for i, cuaca in enumerate(cuacas):
                        local_dt = datetime.datetime.fromisoformat(cuaca["local_datetime"])
                        
                        # Check if this is current weather (within 3 hours behind current time)
                        if check_current_cuaca(str(now), str(local_dt)):
                            if "hujan" in cuaca['weather_desc'].lower():
                                current_raining = True
                                current_index = i
                            break
                    
                    # If not currently raining, return False
                    if not current_raining:
                        return "Ada yang bertanya kepada kamu, kapan hujan reda. Padahal sekarang ga hujan sama sekali. Jawab kalo sekarang lagi gak hujan kok, jadi ga perlu nanya kapan reda."
                    
                    # If currently raining, look for when it will stop
                    for i in range(current_index + 1, len(cuacas)):
                        cuaca = cuacas[i]
                        local_dt = datetime.datetime.fromisoformat(cuaca["local_datetime"])
                        
                        # Find first weather condition without "hujan"
                        if "hujan" not in cuaca['weather_desc'].lower():
                            cuaca_result_not_rain = f"Ada yang bertanya kepada kamu, kapan hujan reda. Dan ini adalah hasil waktu hujan dari data dari BMKG: {local_dt.hour:02}-{local_dt.minute:02}: {cuaca['weather_desc']}"
                            return cuaca_result_not_rain
                    
                    # If rain doesn't stop in the forecast period
                    return "Ada yang bertanya kepada kamu, kapan hujan reda. Tapi kamu belum bisa memastikan kapan reda karena belum mendapat data."
                    
    except Exception as e:
        return f"Error: get_weather_when_stop_rain_by_univ - {str(e)}"
        
def check_current_cuaca(now: str, check_datetime: str) -> bool:
    # Parse the strings into datetime objects
    now_dt = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S.%f")
    check_dt = datetime.datetime.strptime(check_datetime, "%Y-%m-%d %H:%M:%S")
    
    # Calculate time difference
    time_difference = now_dt - check_dt
    
    # Priority 1: Check for past data within 3 hours (prefer recent past data)
    if time_difference >= datetime.timedelta(0) and time_difference <= datetime.timedelta(hours=3):
        return True
    
    # Priority 2: If no past data found, check for future data within 3 hours
    future_time_difference = check_dt - now_dt
    if future_time_difference >= datetime.timedelta(0) and future_time_difference <= datetime.timedelta(hours=3):
        return True
    
    return False