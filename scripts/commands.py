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
from constants import lang, prompts, input_state
from scripts.worker import worker

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
        await asyncio.sleep(10)
        ticking_number_in_second += 10
        
        # run worker function
        # reset ticking_number_in_second
        if ticking_number_in_second >= 3600:
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