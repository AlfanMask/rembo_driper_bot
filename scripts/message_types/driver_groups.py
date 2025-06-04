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
from constants import lang, prompts, drivers
from instances import openrouter, client

# load all env variables
load_dotenv()
import os
# setup gemini ai instance
bot_usn = os.getenv("BOT_USERNAME")
admin_id = os.getenv("ADMIN_ID")
uns_group_chat_id = os.getenv("GROUP_CHAT_ID_UNS")

from helper import weather, text
from constants import univs, groups, statuses

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
        is_admin = True if message.from_user.id == int(admin_id) else False
        user_id: int = message.from_user.id
        nickname = drivers.nicknames.get(user_id)
        if nickname == None:
            nickname = "kak"
            
        # check if asking for weahter information
        is_asking_cuaca: bool = False
        cuaca_result_now: tuple[str, str|None] = ["",""]
        cuaca_result_future: tuple[str, str|None] = ["",""]
        user_group_id = message.chat.id
        user_univ = next((key for key, value in groups.group_chat_ids.items() if value == str(user_group_id)), None)
        if "cuaca" in message.text and "reda" not in message.text:
            (cuaca_result_now, cuaca_result_future) = await weather.get_weather_by_univ(user_univ)
            is_asking_cuaca = True
        
        if "reda" in message.text:
            cuaca_result_future = await weather.get_weather_when_stop_rain_by_univ(user_univ)
            is_asking_cuaca = True
        
        if message_type in ["group", "supergroup"]:
            if message.text:
                # get message from user
                message_from_user = message.text.replace(bot_usn, "")

                # check if user answering message from bot
                is_replying_bot = False
                if message.reply_to_message != None:
                    is_replying_bot = True if message.reply_to_message.from_user.username == bot_usn.replace("@","") else False
                    
                # Indicate bot is typing for 5 seconds
                try:
                    msg_thread_id_rembo:int = int(groups.group_chat_play_rembo_ids[user_univ])
                    await bot.send_chat_action(chat_id=user_group_id, action="typing", message_thread_id=msg_thread_id_rembo)
                except Exception as e:
                    print(e)
                    
                # reply message using gemini AI
                replied_msg = None
                if (bot_usn in message.text):
                    # if admin ask rembo to kick drivers inactive
                    if is_admin and "kick driver" in message.text:
                        await message.reply(statuses.kick_drivers_inactive_start, parse_mode="Markdown")
                        await kick_drivers_inactive()
                        await message.reply(statuses.kick_drivers_inactive_end, parse_mode="Markdown")
                        return
                    
                    is_reply_from_someone = message.reply_to_message
                    if is_reply_from_someone:
                        prev_context = message.reply_to_message.text
                        replied_msg = await openrouter.response(prompts.reply_message_from_user_on_replying_prev_context__driver_group(message_from_user, history_context, prev_context, is_admin, nickname, is_asking_cuaca, cuaca_result_now, cuaca_result_future))
                    else:
                        replied_msg = await openrouter.response(prompts.reply_message_from_user__driver_group(message_from_user, history_context, is_admin, nickname, is_asking_cuaca, cuaca_result_now, cuaca_result_future))
                elif is_replying_bot:
                    prev_context = message.reply_to_message.text
                    replied_msg = await openrouter.response(prompts.reply_message_from_user_on_replying_prev_context__driver_group(message_from_user, history_context, prev_context, is_admin, nickname, is_asking_cuaca, cuaca_result_now, cuaca_result_future))
                
                if replied_msg != None:
                    await message.reply(text.fix_markdown(replied_msg), parse_mode="Markdown")
                    await update_history_ctx(message_from_user)
                    await update_history_ctx(replied_msg)
    except Exception as e:
        print(f"driver_groups.do error: {e}")
        logging.error(f"{datetime.datetime.now()} - [driver_groups.do] Error: {e}")
            
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
    
    
async def kick_drivers_inactive() -> None:
    inactive_driver_ids = client.client.drivers.get.driver_ids_of_inactive_drivers()
    for driver_id in inactive_driver_ids:
        try:
            await bot.ban_chat_member(chat_id=uns_group_chat_id, user_id=driver_id, request_timeout=300) # FOR NOW, only for UNS is enough
            await asyncio.sleep(0.1)
        except Exception as e:
            # if flood exceeded -> pause for 30s
            print(f"{e}: {driver_id}")
            if "Flood control exceeded" in str(e):
                await asyncio.sleep(30)