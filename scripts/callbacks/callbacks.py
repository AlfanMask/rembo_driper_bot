import os, sys, logging, datetime

# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

sys.path.insert(0, project_root)

# aiogram lib
from aiogram import types

# import modules
from instances.dp import dp
from instances.bot import bot
from instances.client import client
from constants import lang, input_state
from keyboards import *

# callbacks
from callbacks.cbs import cb_setting


# callback query using aiogram
@dp.callback_query()
async def callback(callback_query: types.CallbackQuery) -> None:
    user_id: str = str(callback_query.from_user.id)
    data: str = callback_query.data
    message_id: int = callback_query.message.message_id
    
    await callback_query.answer()

    # flag
    keyboard_flag: str = data.rsplit("-", 1)[-1]
    cb_value: str = data.split("-", 1)[0]
    
    # check flags and load the corresponding function
    if keyboard_flag == input_state.flag_setting_pref_ai:
        await cb_setting.do(
            user_id=user_id,
            user_lang=lang.id,
            data=cb_value,
            message_id=message_id,            
        )