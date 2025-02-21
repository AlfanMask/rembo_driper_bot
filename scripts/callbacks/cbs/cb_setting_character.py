import logging, datetime

from constants import input_state, lang, statuses, ai_assistant_default_preference_character
from instances.bot import bot
from instances.client import client
from keyboards import set_close_keyboard

async def do(user_id: str, user_lang: lang, data: str, message_id: str) -> None:
    # close keyboard markup
    kb_close = set_close_keyboard()

    # reset input state
    client.users.delete.input_state_by_user_id(user_id)
    if data == input_state.default[lang.id]:
        client.users.update.preference_ai_by_user_id(user_id, ai_assistant_default_preference_character.default)

        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                reply_markup=kb_close,
                text=statuses.msg_default_setting_character,
                parse_mode="HTML",
            )
        except Exception as e:
            print(f"cb_setting_character {e}")
            logging.error(f"{datetime.datetime.now()} - cb_setting_character {e}")
    elif data == input_state.close[lang.id]:
        try:
            await bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                reply_markup=kb_close,
                text=statuses.msg_cancel_setting_character,
            )
        except Exception as e:
            print(f"cb_setting_character {e}")
            logging.error(f"{datetime.datetime.now()} - cb_setting_character {e}")
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
            print(f"cb_setting_character {e}")
            logging.error(f"{datetime.datetime.now()} - cb_setting_character {e}")