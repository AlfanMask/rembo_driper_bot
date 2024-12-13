import logging, datetime
from scripts.instances.bot import bot
from scripts.instances.gemini_ai import model
from constants import prompts, univs, groups

async def send_motivation(peak_hour_ctx: any=None):
    try:
        response = model.generate_content(prompts.active_driver_motivation(peak_hour_ctx))
        await bot.send_message(
            chat_id=groups.group_chat_ids[univs.uns], # FOR NOW: only send to uns
            text=response.text,
            parse_mode="Markdown",
            request_timeout=300,
        )
    except Exception as e:
        print(f"error: {e}")
        logging.error(f"{datetime.datetime.now()} - Error: {e}")
        
async def announce_many_orders_dont_get_driver():
    try:
        response = model.generate_content(prompts.many_orders_dont_get_driver())
        await bot.send_message(
            chat_id=groups.group_chat_ids[univs.uns], # FOR NOW: only send to uns
            text=response.text,
            parse_mode="Markdown",
            request_timeout=300,
        )
    except Exception as e:
        print(f"error: {e}")
        logging.error(f"{datetime.datetime.now()} - Error: {e}")
        
async def announce_anjem_dont_get_driver(link: str, order_msg: str, univ: univs):
    try:
        response = model.generate_content(prompts.anjem_dont_get_driver(order_msg.replace("#ANJEM","")))
        await bot.send_message(
            chat_id=groups.group_chat_ids[univ],
            text=f"{response.text}👉 {link}",
            parse_mode="Markdown",
            request_timeout=300,
        )
    except Exception as e:
        print(f"error: {e}")
        logging.error(f"{datetime.datetime.now()} - Error: {e}")