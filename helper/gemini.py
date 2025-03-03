import logging, datetime
from aiogram import Router, types
from scripts.instances.bot import bot
from scripts.instances.gemini_ai import model
from constants import prompts, univs, groups

async def send_motivation(peak_hour_ctx: any=None):
    try:
        response = model.generate_content(prompts.active_driver_motivation(peak_hour_ctx))
        await bot.send_message(
            # chat_id=groups.group_chat_ids[univs.uns], # FOR NOW: only send to uns
            chat_id=groups.group_chat_ids[univs.uns], # FOR NOW: only send to uns
            message_thread_id=2,
            text=response.text,
            parse_mode="Markdown",
            request_timeout=300,
        )
    except Exception as e:
        print(f"send_motivation error: {e}")
        logging.error(f"{datetime.datetime.now()} - Error: {e}")
        
async def announce_many_orders_dont_get_driver():
    try:
        response = model.generate_content(prompts.many_orders_dont_get_driver())
        sent_message:types.Message = await bot.send_message(
            chat_id=groups.group_chat_ids[univs.uns], # FOR NOW: only send to uns
            text=response.text,
            parse_mode="Markdown",
            request_timeout=300,
        )
        await bot.pin_chat_message(
            chat_id=groups.group_chat_ids[univs.uns],
            message_id=sent_message.message_id,
        )
    except Exception as e:
        print(f"announce_many_orders_dont_get_driver error: {e}")
        logging.error(f"{datetime.datetime.now()} - Error: {e}")
        
async def announce_anjem_dont_get_driver(link: str, order_msg: str, univ: univs):
    try:
        # send to group + pin
        response = model.generate_content(prompts.anjem_dont_get_driver(order_msg.replace("#ANJEM","")))
        sent_message:types.Message = await bot.send_message(
            chat_id=groups.group_chat_ids[univ],
            text=f"{response.text}👉 {link}",
            parse_mode="Markdown",
            request_timeout=300,
        )
        await bot.pin_chat_message(
            chat_id=groups.group_chat_ids[univ],
            message_id=sent_message.message_id,
        )
    except Exception as e:
        print(f"announce_anjem_dont_get_driver error: {e}")
        logging.error(f"{datetime.datetime.now()} - Error: {e}")
        
async def announce_will_rain(univ: univs):
    try:
        response = model.generate_content(prompts.announce_will_rain())
        await bot.send_message(
            chat_id=groups.group_chat_ids[univ],
            text=response.text,
            parse_mode="Markdown",
            request_timeout=300,
        )
    except Exception as e:
        print(f"announce_many_orders_dont_get_driver error: {e}")
        logging.error(f"{datetime.datetime.now()} - Error: {e}")