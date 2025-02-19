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
    # if last_update_history > 5 minutes -> clear history_context
    global history_context
    global last_update_history
    if datetime.datetime.now() - last_update_history > datetime.timedelta(minutes=5):
        history_context = []
    
    message_type: str = message.chat.type
    is_admin = True if (message.from_user.id == int(admin_id) or message.from_user.is_bot) else False
    user_id: int = message.from_user.id
    nickname = drivers.nicknames.get(user_id)
    if nickname == None:
        nickname = "kak"
    
    if message_type in ["group", "supergroup"]:
        if message.text:
            # get message from user
            message_from_user = message.text.replace(bot_usn, "")

            # get post context so AI know what is he mentioned to if needed
            post_context = message.reply_to_message.text or message.reply_to_message.caption or ""

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
                    replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__menfess_comment(message_from_user, history_context, prev_context, is_admin, nickname, post_context))
                else:
                    replied_msg = model.generate_content(prompts.reply_message_from_user__menfess_comment(message_from_user, history_context, is_admin, nickname, post_context))
            elif is_replying_bot:
                prev_context = message.reply_to_message.text
                replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__menfess_comment(message_from_user, history_context, prev_context, is_admin, nickname, post_context))
            
            if replied_msg != None:
                await message.reply(replied_msg.text, parse_mode="Markdown")
                await update_history_ctx(message_from_user)
                await update_history_ctx(replied_msg.text)
            
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