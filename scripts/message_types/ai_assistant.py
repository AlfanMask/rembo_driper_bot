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
from scripts.instances import openrouter

# load all env variables
load_dotenv()
import os
# setup gemini ai instance
bot_usn = os.getenv("BOT_USERNAME")
admin_id = os.getenv("ADMIN_ID")

# TODO: make history context for each users. make on database
# TODO: replace [] on arguments with correct context history
async def do(message: types.Message):    
    is_admin = True if (message.from_user.id == int(admin_id) or message.from_user.is_bot) else False
    user_id: int = message.from_user.id
    nickname = drivers.nicknames.get(user_id)
    if nickname == None:
        nickname = "kak"
    
    # get message from user
    message_from_user = message.text.replace(bot_usn, "")

    # check if user answering message from bot
    is_replying_bot = False
    if message.reply_to_message != None:
        is_replying_bot = True if message.reply_to_message.from_user.username == bot_usn.replace("@","") else False
        
    # reply message using DeepSeek AI
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing") # make bot is typing
    replied_msg = None
    if is_replying_bot:
        prev_context = message.reply_to_message.text
        replied_msg = await openrouter.response(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant(message_from_user, [], prev_context, is_admin, nickname))
    else:
        is_reply_from_someone = message.reply_to_message
        if is_reply_from_someone:
            prev_context = message.reply_to_message.text
            replied_msg = await openrouter.response(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant(message_from_user, [], prev_context, is_admin, nickname))
        else:
            replied_msg = await openrouter.response(prompts.reply_message_from_user__ai_assistant(message_from_user, [], is_admin, nickname))
    
    if replied_msg != None:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=replied_msg,
            parse_mode="Markdown"
        )