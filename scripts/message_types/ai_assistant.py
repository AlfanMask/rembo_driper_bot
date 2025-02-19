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
from constants import lang, prompts, drivers, ai_assistant_message_type
from scripts.instances import openrouter
from scripts.instances.client import client

# load all env variables
load_dotenv()
import os
# setup gemini ai instance
bot_usn = os.getenv("BOT_USERNAME")
admin_id = os.getenv("ADMIN_ID")

async def do(message: types.Message):    
    is_admin = True if (message.from_user.id == int(admin_id) or message.from_user.is_bot) else False
    user_id: int = message.from_user.id
    nickname = drivers.nicknames.get(user_id)
    if nickname == None:
        nickname = "kak"
    
    # get message from user
    if message.text:
        message_from_user = message.text.replace(bot_usn, "")

        # check if user answering message from bot
        is_replying_bot = False
        if message.reply_to_message != None:
            is_replying_bot = True if message.reply_to_message.from_user.username == bot_usn.replace("@","") else False
            
        # get history context of last 20 chats (request response from database)
        history_context: list[str] = client.ai_assistant_messages.get.last_20_chats_from_user_id(user_id)

        # get user's ai assistant preference character
        pref_ai_character = client.users.get.active_preference_ai(user_id)
            
        # reply message using DeepSeek AI
        await bot.send_chat_action(chat_id=message.from_user.id, action="typing") # make bot is typing
        replied_msg = None
        if is_replying_bot:
            prev_context = message.reply_to_message.text
            replied_msg = await openrouter.response(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant(message_from_user, history_context, prev_context, is_admin, nickname, pref_ai_character))
        else:
            is_reply_from_someone = message.reply_to_message
            if is_reply_from_someone:
                prev_context = message.reply_to_message.text
                replied_msg = await openrouter.response(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant(message_from_user, history_context, prev_context, is_admin, nickname, pref_ai_character))
            else:
                replied_msg = await openrouter.response(prompts.reply_message_from_user__ai_assistant(message_from_user, history_context, is_admin, nickname, pref_ai_character))
        
        if replied_msg != None:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=replied_msg,
                parse_mode="Markdown"
            )
            
        # save chats (request & response) to database to be used as history context
        client.ai_assistant_messages.create.new(user_id, ai_assistant_message_type.request, message_from_user)
        client.ai_assistant_messages.create.new(user_id, ai_assistant_message_type.response, replied_msg)