import os, sys, logging, datetime, asyncio
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
from constants import lang, prompts, drivers, ai_assistant_message_type, statuses, ai_assistant_mode
# from scripts.instances import openrouter
from scripts.instances.gemini_ai import model
from scripts.instances.client import client
from helper import text

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
        
        # Get message from user
        if message.text:
            message_from_user = message.text.replace(bot_usn, "")

            # Check if user is replying to bot
            is_replying_bot = False
            if message.reply_to_message and message.reply_to_message.from_user:
                is_replying_bot = message.reply_to_message.from_user.username == bot_usn.replace("@", "")
            
            # Get user's AI assistant preference character
            pref_ai_character = client.users.get.active_preference_ai(user_id)
            
            # Indicate bot is typing + await for 3 seconds
            await bot.send_chat_action(chat_id=user_id, action="typing")
            await asyncio.sleep(3)
            
            # Generate response using Gemini AI
            replied_msg = None

            ai_mode: ai_assistant_mode = client.users.get.ai_mode_by_user_id(user_id)
            history_context = client.ai_assistant_messages.get.last_20_chats_from_user_id(user_id, ai_mode)
            
            if is_replying_bot:
                prev_context = message.reply_to_message.text
                try:
                    replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant_chatting(message_from_user, history_context, prev_context, is_admin, nickname, pref_ai_character, ai_mode)) if ai_mode in [ai_assistant_mode.chatting_fun, ai_assistant_mode.chatting_short] else model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant_serious(message_from_user, history_context, prev_context))
                except Exception as e:
                    print(f"ai_assistant.do.is_replying_bot error: {e}")
                    logging.error("ai_assistant.do.is_replying_bot error: %s", str(e), exc_info=True)
                    await show_error(user_id)
                    return
            else:
                is_reply_from_someone = message.reply_to_message is not None
                if is_reply_from_someone:
                    prev_context = message.reply_to_message.text
                    try:
                        replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant_chatting(message_from_user, history_context, prev_context, is_admin, nickname, pref_ai_character, ai_mode)) if ai_mode in [ai_assistant_mode.chatting_fun, ai_assistant_mode.chatting_short] else model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__ai_assistant_serious(message_from_user, history_context, prev_context))
                    except Exception as e:
                        print(f"ai_assistant.do.!is_replying_bot.is_reply_from_someone error: {e}")
                        logging.error("ai_assistant.do.!is_replying_bot.is_reply_from_someone error: %s", str(e), exc_info=True)
                        await show_error(user_id)
                        return
                else:
                    try:
                        replied_msg = model.generate_content(prompts.reply_message_from_user__ai_assistant_chatting(message_from_user, history_context, is_admin, nickname, pref_ai_character, ai_mode)) if ai_mode in [ai_assistant_mode.chatting_fun, ai_assistant_mode.chatting_short] else model.generate_content(prompts.reply_message_from_user__ai_assistant_serious(message_from_user, history_context))
                    except Exception as e:
                        print(f"ai_assistant.do.!is_replying_bot.!is_reply_from_someone error: {e}")
                        logging.error("ai_assistant.do.!is_replying_bot.!is_reply_from_someone error: %s", str(e), exc_info=True)
                        await show_error(user_id)
                        return
            try:
                if replied_msg:
                    try:
                        await bot.send_message(
                            chat_id=user_id,
                            text=text.fix_markdown(replied_msg.text),
                            parse_mode="Markdown"
                        )
                    except Exception as e:
                        if "can't parse entities" in str(e):
                            await bot.send_message(
                                chat_id=user_id,
                                text=replied_msg.text,
                                parse_mode="HTML"
                            )
                    
                # Save chats (request & response) to database
                client.ai_assistant_messages.create.new(user_id, ai_assistant_message_type.request, message_from_user, ai_mode)
                client.ai_assistant_messages.create.new(user_id, ai_assistant_message_type.response, replied_msg.text, ai_mode)
            except Exception as e:
                print(f"ai_assistant.do error: {e}")
                logging.error("ai_assistant.do error: %s", str(e), exc_info=True)
                await show_error(user_id)
                return
            
    except Exception as e:
        logging.error("ai_assistant.do error: %s", str(e), exc_info=True)
        print(f"ai_assistant.do error: {e}")

async def show_error(user_id: str) -> None:
    try:
        await bot.send_message(
            chat_id=user_id,
            text=statuses.error_ai_busy,
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"ai_assistant.show_error error: {e}")
        logging.error("ai_assistant.show_error error: %s", str(e), exc_info=True)