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
from constants import lang, prompts, drivers, input_state, statuses
from instances.gemini_ai import model

# load all env variables
load_dotenv()
import os
# setup gemini ai instance
bot_usn = os.getenv("BOT_USERNAME")
admin_id = os.getenv("ADMIN_ID")
from helper import weather
from constants import univs, groups
from message_types import driver_groups, ai_assistant, menfess_comment
from scripts.instances.client import client

# handle bot to reply message
@dp.message()
async def handler_msg_reply(message: types.Message) -> None:
    try:
        if message.text:        
            # only proceed if private (so prevent users comment on post discussion and the text is transfered here)
            # if handling input_state of this bot
            user_input_state = client.users.get.input_state_by_user_id(message.from_user.id)
            ai_assistant_input_states: list[str] = [input_state.input_setting_ref_ai]
            if user_input_state in ai_assistant_input_states and message.chat.type == "private":
                await process_user_input_state(message.from_user.id, user_input_state, message.text)
                return

            # always reset input_state
            client.users.delete.input_state_by_user_id(message.from_user.id)
            
            # MAKE 3 TYPES OF MESSAGES: Driver Group discussion, Personal Chat AI Assistent, and Menfess comment
            # == Driver Group Discussion
            if f"-100{str(message.chat.id).replace('-100','').replace('-','')}" in groups.group_chat_ids.values():
                await driver_groups.do(message)
            
            # == Personal Chat AI Assistant
            elif message.chat.type == "private":
                await ai_assistant.do(message)
            
            # == Menfess comment
            else:
                await menfess_comment.do(message)
    except Exception as e:
        print(f"handler_msg_reply error: {e}")
        logging.error(f"{datetime.datetime.now()} - [messages.handler_msg_reply] Error: {e}")
        
        
# USER INPUT STATES
async def process_user_input_state(user_id: str, user_input_state: str, message: str) -> None:
    try:
        if user_input_state == input_state.input_setting_ref_ai:
            await update_preference_ai(user_id, message)
    except Exception as e:
        print(f"process_user_input_state error: {e}")
        logging.error(f"{datetime.datetime.now()} - [messages.process_user_input_state] Error: {e}")

async def update_preference_ai(user_id: str, pref_ai: str) -> None:
    try:
        # update user's preference ai character
        client.users.update.preference_ai_by_user_id(user_id, pref_ai.replace('"', ''))
        client.users.delete.input_state_by_user_id(user_id)

        await bot.send_message(
            chat_id=user_id,
            text=statuses.msg_success_setting_character(pref_ai),
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"update_preference_ai error: {e}")
        logging.error(f"{datetime.datetime.now()} - [messages.update_preference_ai] Error: {e}")