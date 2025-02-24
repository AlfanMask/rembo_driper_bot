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
from constants import input_state, lang, ai_assistant_mode

def set_setting_preference_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=input_state.default[lang.id], callback_data=f"{input_state.default[lang.id]}-{input_state.flag_setting_pref_ai}")],
        [InlineKeyboardButton(text=input_state.close[lang.id], callback_data=f"{input_state.close[lang.id]}-{input_state.flag_setting_pref_ai}")],
    ])
    
    return keyboard

def set_setting_mode_keyboard(active_mode: ai_assistant_mode) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"{input_state.chatting_fun[lang.id]} {'✅' if active_mode == ai_assistant_mode.chatting_fun else ''}", callback_data=f"{input_state.chatting_fun[lang.id]}-{input_state.flag_setting_mode_ai}"),
            InlineKeyboardButton(text=f"{input_state.chatting_short[lang.id]} {'✅' if active_mode == ai_assistant_mode.chatting_short else ''}", callback_data=f"{input_state.chatting_short[lang.id]}-{input_state.flag_setting_mode_ai}"),
        ],
        [InlineKeyboardButton(text=f"{input_state.serious[lang.id]} {'✅' if active_mode == ai_assistant_mode.serious else ''}", callback_data=f"{input_state.serious[lang.id]}-{input_state.flag_setting_mode_ai}")],
    ])
    
    return keyboard

# keyboard: for clean up
def set_close_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    return keyboard