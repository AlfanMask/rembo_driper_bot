import logging, datetime

from constants import input_state, lang, statuses, ai_assistant_mode
from instances.bot import bot
from instances.client import client
from keyboards import set_close_keyboard, set_setting_mode_keyboard

async def do(user_id: str, user_lang: lang, data: str, message_id: str) -> None:
    if data == input_state.chatting_fun[lang.id]:
        client.users.update.mode_ai_by_user_id(user_id, ai_assistant_mode.chatting_fun)

        kb_mode = set_setting_mode_keyboard(ai_assistant_mode.chatting_fun)

        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                reply_markup=kb_mode,
                text=statuses.msg_setting_mode(),
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"cb_setting_mode {e}")
            logging.error(f"{datetime.datetime.now()} - cb_setting_mode {e}")
    elif data == input_state.chatting_short[lang.id]:
        client.users.update.mode_ai_by_user_id(user_id, ai_assistant_mode.chatting_short)

        kb_mode = set_setting_mode_keyboard(ai_assistant_mode.chatting_short)

        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                reply_markup=kb_mode,
                text=statuses.msg_setting_mode(),
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"cb_setting_mode {e}")
            logging.error(f"{datetime.datetime.now()} - cb_setting_mode {e}")
    elif data == input_state.serious[lang.id]:
        client.users.update.mode_ai_by_user_id(user_id, ai_assistant_mode.serious)

        kb_mode = set_setting_mode_keyboard(ai_assistant_mode.serious)

        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                reply_markup=kb_mode,
                text=statuses.msg_setting_mode(),
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"cb_setting_mode {e}")
            logging.error(f"{datetime.datetime.now()} - cb_setting_mode {e}")
    else:
        # set input_state for current user to set_age
        client.users.delete.input_state_by_user_id(user_id)

        try:
            await bot.send_message(
                chat_id=user_id,
                text=input_state.error_input[user_lang],
                parse_mode="Markdown",
            )
        except Exception as e:
            print(f"cb_setting_mode {e}")
            logging.error(f"{datetime.datetime.now()} - cb_setting_mode {e}")