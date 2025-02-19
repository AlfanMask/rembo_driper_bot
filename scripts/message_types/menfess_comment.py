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

# messages history context: 10 of latest request (5) and response (5) data as context reference
global history_context
history_context: list[str] = []
global last_update_history
last_update_history = datetime.datetime.now()

async def do(message: types.Message):
    try:
        global history_context
        global last_update_history
        
        logging.debug("Received message: %s", message.text)
        
        # Check and clear history context if needed
        if last_update_history and datetime.datetime.now() - last_update_history > datetime.timedelta(minutes=5):
            logging.info("Clearing history context due to inactivity.")
            history_context = []
        
        message_type: str = message.chat.type
        user_id: int = message.from_user.id
        is_admin = user_id == int(admin_id) or message.from_user.is_bot
        nickname = drivers.nicknames.get(user_id, "kak")
        
        logging.debug("Message type: %s, User ID: %d, Is Admin: %s, Nickname: %s", message_type, user_id, is_admin, nickname)
        
        if message_type in ["group", "supergroup"]:
            if message.text:
                message_from_user = message.text.replace(bot_usn, "")
                
                logging.debug("Processed user message: %s", message_from_user)
                
                # Get post context
                post_context = ""
                if message.reply_to_message:
                    if message.reply_to_message.text:
                        post_context = message.reply_to_message.text
                    elif message.reply_to_message.caption:
                        post_context = message.reply_to_message.caption
                
                logging.debug("Post context: %s", post_context)
                
                # Check if the user is replying to the bot
                is_replying_bot = False
                if message.reply_to_message:
                    if message.reply_to_message.from_user:
                        is_replying_bot = message.reply_to_message.from_user.username == bot_usn.replace("@", "")
                
                logging.debug("Is replying to bot: %s", is_replying_bot)
                
                replied_msg = None
                if bot_usn in message.text:
                    if message.reply_to_message:
                        prev_context = message.reply_to_message.text if message.reply_to_message.text else ""
                        logging.debug("Previous context in reply: %s", prev_context)
                        replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__menfess_comment(message_from_user, history_context, prev_context, is_admin, nickname, post_context))
                    else:
                        replied_msg = model.generate_content(prompts.reply_message_from_user__menfess_comment(message_from_user, history_context, is_admin, nickname, post_context))
                elif is_replying_bot:
                    prev_context = message.reply_to_message.text if message.reply_to_message.text else ""
                    logging.debug("Previous context from bot reply: %s", prev_context)
                    replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__menfess_comment(message_from_user, history_context, prev_context, is_admin, nickname, post_context))
                
                if replied_msg:
                    logging.info("Replying with message: %s", replied_msg.text)
                    await message.reply(replied_msg.text, parse_mode="Markdown")
                    await update_history_ctx(message_from_user)
                    await update_history_ctx(replied_msg.text)
    except Exception as e:
        logging.error("ai_assistant.do error: %s", str(e), exc_info=True)
        print(f"ai_assistant.do error: {e}")
            
async def update_history_ctx(text: str) -> None:
    global history_context
    global last_update_history

    # put message to history context
    history_context.append(text)

    # delete first item if lenght >= 10
    if len(history_context) > 10:
        del history_context[0]
        
    # update history timestamp
    last_update_history = datetime.datetime.now()