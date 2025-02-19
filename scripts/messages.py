import os, sys, logging, datetime
from dotenv import load_dotenv
# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

sys.path.insert(0, project_root)

# aigrom lib
from aiogram import Router, types

# import modules
from instances.bot import bot
from instances.dp import dp
from constants import lang, prompts, drivers
from instances.gemini_ai import model

# load all env variables
load_dotenv()
import os
# setup gemini ai instance
bot_usn = os.getenv("BOT_USERNAME")
admin_id = os.getenv("ADMIN_ID")
from helper import weather
from constants import univs, groups
from message_types import driver_groups, menfess_comment

# handle bot to reply message
@dp.message()
async def handler_msg_reply(message: types.Message) -> None:
    # MAKE 3 TYPES OF MESSAGES: Driver Group discussion, Personal Chat AI Assistent, and Menfess comment
    
    # == Driver Group Discussion
    if f"-100{str(message.chat.id).replace('-','')}" in groups.group_chat_ids.values():
        await driver_groups.do(message)
    
    # == Personal Chat AI Assistant
    elif message.chat.type == "private":
        # TODO:
        pass
    
    # == Menfess comment
    else:
        await menfess_comment.do(message)