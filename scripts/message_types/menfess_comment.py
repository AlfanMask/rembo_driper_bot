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
from constants import lang, prompts, drivers, statuses
from instances.gemini_ai import model
from helper import text

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
                    
                # await for 3 seconds
                await asyncio.sleep(3)
                    
                # reply message using gemini AI
                replied_msg = None
                if (bot_usn in message.text):
                    is_reply_from_someone = message.reply_to_message
                    if is_reply_from_someone:
                        try:
                            prev_context = message.reply_to_message.text
                            replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__menfess_comment(message_from_user, history_context, prev_context, is_admin, nickname, post_context))
                        except Exception as e:
                            print(f"menfess_comment.do.[bot_usn in message.text].is_reply_from_someone error: {e}")
                            logging.error("menfess_comment.do.[bot_usn in message.text].is_reply_from_someone error: %s", str(e), exc_info=True)
                            await show_error(user_id)
                            return
                    else:
                        try:
                            replied_msg = model.generate_content(prompts.reply_message_from_user__menfess_comment(message_from_user, history_context, is_admin, nickname, post_context))
                        except Exception as e:
                            print(f"menfess_comment.do.[bot_usn in message.text].!is_reply_from_someone error: {e}")
                            logging.error("menfess_comment.do.[bot_usn in message.text].!is_reply_from_someone error: %s", str(e), exc_info=True)
                            await show_error(user_id)
                            return
                elif is_replying_bot:
                    try:
                        prev_context = message.reply_to_message.text
                        replied_msg = model.generate_content(prompts.reply_message_from_user_on_replying_prev_context__menfess_comment(message_from_user, history_context, prev_context, is_admin, nickname, post_context))
                    except Exception as e:
                            print(f"menfess_comment.do.is_replying_bot error: {e}")
                            logging.error("menfess_comment.do.is_replying_bot error: %s", str(e), exc_info=True)
                            await show_error(user_id)
                            return
                try:
                    if replied_msg != None:
                        await message.reply(text.fix_markdown(replied_msg.text), parse_mode="Markdown")
                        await update_history_ctx(message_from_user)
                        await update_history_ctx(replied_msg.text)
                except Exception as e:
                    print(f"menfess_comment.do error: {e}")
                    logging.error("menfess_comment.do error: %s", str(e), exc_info=True)
                    await show_error(user_id)
                    return
    except Exception as e:
        print(f"menfess_comment.do error: {e}")
        logging.error(f"{datetime.datetime.now()} - [menfess_comment.do] Error: {e}")
            
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
    
async def show_error(user_id: str) -> None:
    try:
        await bot.send_message(
            chat_id=user_id,
            text=statuses.error_ai_busy,
            parse_mode="HTML",
        )
    except Exception as e:
        print(f"menfess_comment.show_error error: {e}")
        logging.error("menfess_comment.show_error error: %s", str(e), exc_info=True)