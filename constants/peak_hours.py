from typing import Final
import datetime

ph_list: Final[dict] = {
    "a": datetime.time(6, 30),
    # "b": datetime.time(9, 0), # FOR NOW disable b & d, also it's disabled in prompts.py for ph_list["b"] and ph_list["d"]
    "c": datetime.time(12, 0),
    # "d": datetime.time(15, 0),
    "e": datetime.time(19, 0),
}