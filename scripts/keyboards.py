import os
import sys
# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

sys.path.insert(0, project_root)

# aiogram lib
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# import modules
from constants import input_state, lang

def set_setting_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=input_state.default[lang.id], callback_data=f"{input_state.default[lang.id]}-{input_state.flag_setting_pref_ai}")],
        [InlineKeyboardButton(text=input_state.close[lang.id], callback_data=f"{input_state.close[lang.id]}-{input_state.flag_setting_pref_ai}")],
    ])
    
    return keyboard

# keyboard: for clean up
def set_close_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    return keyboard