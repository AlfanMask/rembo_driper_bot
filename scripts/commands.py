import os, sys, datetime, asyncio
# get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))
sys.path.insert(0, project_root)

# aigrom lib
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

# import modules
from instances.bot import bot
from instances.dp import dp
from instances.logger import bot_logger
# from scripts.instances.db import db
from scripts import keyboards
from constants import statuses, input_state
from scripts.worker import worker
from scripts.instances.client import client
from scripts import keyboards
from helper import gemini

"""
## ADMIN commands
"""

# For ticking count
global ticking_number_in_second
ticking_number_in_second: int = 0
ticking_task = None  # To keep track of the background task

async def tick_counter():
    global ticking_number_in_second
    while True:
        await asyncio.sleep(1)
        ticking_number_in_second += 1
        print(ticking_number_in_second)
        
        # run worker function
        # reset ticking_number_in_second
        if ticking_number_in_second >= 600:
            await worker()
            ticking_number_in_second = 0
            

# Start command
@dp.message(CommandStart())
async def start_command(message: Message):
    global ticking_task
    bot_logger.info(f"{datetime.datetime.now()} - new_user_id: {str(message.from_user.id)}")
    
    # Start ticking task if it's not already running
    if ticking_task is None:
        ticking_task = asyncio.create_task(tick_counter())
    
    await message.answer("Haloo, Rembo di sini kukuruyuukk..")
    
# Give Motivation Directly
@dp.message(Command("motivation"))
async def motivation(message: Message):
    await gemini.send_motivation()
    await message.reply(text="Motivation Sent to the group!")
    
    
# Setting Up AI Assistant Character
@dp.message(Command("karakter"))
async def karakter(message: Message):
    user_id = message.from_user.id
    kb_setting = keyboards.set_setting_preference_keyboard()
    client.users.update.input_state_by_user_id(user_id, input_state.input_setting_ref_ai)

    # send message alert to send the user_id to be deleted input_state
    active_preference = client.users.get.active_preference_ai(user_id)
    try:
        await bot.send_message(
            chat_id=user_id,
            text=statuses.msg_setting_character(active_preference),
            reply_markup=kb_setting,
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"{datetime.datetime.now()} - ERROR - [commands.karakter] - {user_id} - {e}")
        bot_logger.error(f"{datetime.datetime.now()} - [commands.karakter] - {user_id} - {e}")
        
# Setting Up AI Assistant Mode
@dp.message(Command("mode"))
async def mode(message: Message):
    user_id = message.from_user.id
    active_mode = client.users.get.ai_mode_by_user_id(user_id)
    kb_setting = keyboards.set_setting_mode_keyboard(active_mode)
    client.users.delete.input_state_by_user_id(user_id)

    try:
        await bot.send_message(
            chat_id=user_id,
            text=statuses.msg_setting_mode(),
            reply_markup=kb_setting,
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"{datetime.datetime.now()} - ERROR - [commands.mode] - {user_id} - {e}")
        bot_logger.error(f"{datetime.datetime.now()} - [commands.mode] - {user_id} - {e}")
        
# Reset AI Assistant Memory (History Context)
@dp.message(Command("reset"))
async def mode(message: Message):
    user_id = message.from_user.id
    client.users.delete.input_state_by_user_id(user_id)

    try:
        # reset memory of rembo
        client.ai_assistant_messages.update.delete_memory_by_user_id(user_id)
    
        await bot.send_message(
            chat_id=user_id,
            text=statuses.msg_success_reset_memory,
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"{datetime.datetime.now()} - ERROR - [commands.mode] - {user_id} - {e}")
        bot_logger.error(f"{datetime.datetime.now()} - [commands.mode] - {user_id} - {e}")