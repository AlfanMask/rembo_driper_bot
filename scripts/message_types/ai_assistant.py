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
    try:
        user_id: int = message.from_user.id
        is_admin = user_id == int(admin_id) or message.from_user.is_bot
        nickname = drivers.nicknames.get(user_id, "kak")
        
        logging.debug("User ID: %d, Is Admin: %s, Nickname: %s", user_id, is_admin, nickname)
        
        # Get message from user
        if message.text:
            message_from_user = message.text.replace(bot_usn, "")
            logging.debug("Processed user message: %s", message_from_user)

            # Check if user is replying to bot
            is_replying_bot = False
            if message.reply_to_message and message.reply_to_message.from_user:
                is_replying_bot = message.reply_to_message.from_user.username == bot_usn.replace("@", "")
            
            logging.debug("Is replying to bot: %s", is_replying_bot)
            
            # Get history context of last 20 chats
            history_context = client.ai_assistant_messages.get.last_20_chats_from_user_id(user_id)
            logging.debug("History context retrieved: %s", history_context)
            
            # Get user's AI assistant preference character
            pref_ai_character = client.users.get.active_preference_ai(user_id)
            logging.debug("User AI assistant preference: %s", pref_ai_character)
            
            # Indicate bot is typing
            await bot.send_chat_action(chat_id=user_id, action="typing")
            
            # Generate response using DeepSeek AI
            replied_msg = None
            if is_replying_bot:
                prev_context = message.reply_to_message.text
                logging.debug("Previous context in bot reply: %s", prev_context)
                replied_msg = await openrouter.response(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant(message_from_user, history_context, prev_context, is_admin, nickname, pref_ai_character))
            else:
                is_reply_from_someone = message.reply_to_message is not None
                if is_reply_from_someone:
                    prev_context = message.reply_to_message.text
                    logging.debug("Previous context from another user reply: %s", prev_context)
                    replied_msg = await openrouter.response(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant(message_from_user, history_context, prev_context, is_admin, nickname, pref_ai_character))
                else:
                    replied_msg = await openrouter.response(prompts.reply_message_from_user__ai_assistant(message_from_user, history_context, is_admin, nickname, pref_ai_character))
            
            if replied_msg:
                logging.info("Replying with message: %s", replied_msg)
                await bot.send_message(
                    chat_id=user_id,
                    text=replied_msg,
                    parse_mode="Markdown"
                )
                
            # Save chats (request & response) to database
            client.ai_assistant_messages.create.new(user_id, ai_assistant_message_type.request, message_from_user)
            client.ai_assistant_messages.create.new(user_id, ai_assistant_message_type.response, replied_msg)
            logging.info("Saved chat history for user %d", user_id)
    except Exception as e:
        logging.error("driver_groups.do error: %s", str(e), exc_info=True)
        print(f"driver_groups.do error: {e}")
