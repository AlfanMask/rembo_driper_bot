
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
                            cuaca_result_now = f"{local_dt.year}-{local_dt.month}-{local_dt.day} {local_dt.hour:02}-{local_dt.minute:02}-{local_dt.second:02}: {cuaca['weather_desc']}"
                            
                            # Get next item if available
                            if i < len(cuacas) - 1:
                                next_cuaca = cuacas[i + 1]
                                next_local_dt = datetime.datetime.fromisoformat(next_cuaca["local_datetime"])
                                cuaca_result_future = f"{next_local_dt.year}-{next_local_dt.month}-{next_local_dt.day} {next_local_dt.hour:02}-{next_local_dt.minute:02}-{next_local_dt.second:02}: {next_cuaca['weather_desc']}"

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

                    for i, cuaca in enumerate(cuacas):
                        local_dt = datetime.datetime.fromisoformat(cuaca["local_datetime"])

                        # get if not rain
                        if "hujan" in cuaca['weather_desc'].lower():
                            continue
                        else:
                            cuaca_result_not_rain = f"{local_dt.year}-{local_dt.month}-{local_dt.day} {local_dt.hour:02}-{local_dt.minute:02}-{local_dt.second:02}: {cuaca['weather_desc']}"
                            return cuaca_result_not_rain

        return None
    except Exception as e:
        print(f"{e}: error getting weather from weather bmkg data terbuka")
        return None
        
def check_current_cuaca(now: str, check_datetime) -> str:
    # Parse the strings into datetime objects
    now_dt = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M:%S.%f")
    check_dt = datetime.datetime.strptime(check_datetime, "%Y-%m-%d %H:%M:%S")

    # Calculate the time difference
    time_difference = check_dt - now_dt
    
    # Check if now is less than check_datetime and within a 3-hour difference
    if now_dt < check_dt and datetime.timedelta(hours=0) <= time_difference <= datetime.timedelta(hours=3):
        return True
    return False
