from datetime import datetime

def get_day_time_indonesian() -> tuple[str, str]:
    # Map English day names to Indonesian
    hari_map = {
        "Sunday": "Minggu",
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu"
    }
    
    # Get the current day and map to Indonesian
    hari_inggris = datetime.now().strftime("%A")  # e.g., "Sunday", "Monday"
    hari_indonesia = hari_map[hari_inggris]
    
    # Get the current hour
    jam_sekarang = datetime.now().hour
    
    # Determine the time of day
    if 5 <= jam_sekarang < 12:
        waktu_hari = "pagi"
    elif 12 <= jam_sekarang < 15:
        waktu_hari = "siang"
    elif 15 <= jam_sekarang < 18:
        waktu_hari = "sore"
    else:
        waktu_hari = "malam"
    
    return (hari_indonesia, waktu_hari)