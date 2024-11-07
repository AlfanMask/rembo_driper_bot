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
from constants import lang, prompts
from instances.gemini_ai import model

# load all env variables
load_dotenv()
import os
# setup gemini ai instance
bot_usn = os.getenv("BOT_USERNAME")

# handle bot to reply message
@dp.message()
async def handler_msg_reply(message: types.Message) -> None:
    message_type: str = message.chat.type
    if message_type in ["group", "supergroup"]:
        # get message from user
        message_from_user = message.text.replace(bot_usn, "")

        # check if user answering message from bot
        is_replying_bot = False
        if message.reply_to_message != None:
            is_replying_bot = True if message.reply_to_message.from_user.username == bot_usn.replace("@","") else False
            
        # reply message using gemini AI
        replied_msg = None
        if (bot_usn in message.text):
            is_reply_from_someone = message.reply_to_message
            if is_reply_from_someone:
                prev_context = message.reply_to_message.text
                replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context(message_from_user, prev_context))
            else:
                replied_msg = model.generate_content(prompts.reply_message_from_user(message_from_user))
        elif is_replying_bot:
            prev_context = message.reply_to_message.text
            replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context(message_from_user, prev_context))
        
        await message.reply(replied_msg.text, parse_mode="Markdown")