
import aiohttp, datetime
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
                    # check the current cuaca within radius 3 hours
                    cuaca_result_now:str = ""
                    cuaca_result_future:str = ""
                    for i, cuaca in enumerate(cuacas):
                        is_current_cuaca = check_current_cuaca(str(now), str(cuaca["local_datetime"]))
                        if is_current_cuaca:
                            cuaca_result_now = cuaca["weather_desc"]
                            if i < len(cuacas) - 1:
                                cuaca_result_future = cuacas[i+1]["weather_desc"]
                            else:
                                cuaca_result_future = ""
                            break
                    
                    return (cuaca_result_now, cuaca_result_future)
                else:
                    return None
    except Exception as e:
        print(f"{e}: error getting weather from weather bmkg data terbuka")
        
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
