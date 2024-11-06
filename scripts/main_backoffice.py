import asyncio, logging, datetime, sys
from dotenv import load_dotenv

# aigoram utils
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

# load all env variables
load_dotenv()
import os

# import other modules that needed to run
from instances.bot import bot
from instances.dp import dp
from instances.logger import bot_logger
from commands import start_command
from messages import handler_msg_reply

async def main() -> None:
    # log starting poll process
    bot_logger.info(f"{datetime.datetime.now()} - Polling...")
    print("Polling...")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    # log starting bot process
    bot_logger.info(f"{datetime.datetime.now()} - Starting bot...")
    print("Starting bot...")
    
    # run main function
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# async def main() -> None:
#     # log starting poll process
#     bot_logger.info(f"{datetime.datetime.now()} - Polling...")
#     print("Polling...")
    
#     try:
#         await dp.start_polling(bot)
#     except Exception as e:
#         print(e)
#         bot_logger.error(f"{datetime.datetime.now()} - Error: {e}")

# if __name__ == "__main__": 
#     # log starting bot process
#     bot_logger.info(f"{datetime.datetime.now()} - Starting bot...")
#     print("Starting bot...")
    
#     # Create an event loop
#     loop = asyncio.get_event_loop()
    
#     # Run the main function asynchronously
#     main_task = loop.create_task(main())
    
#     # Run the worker function concurrently
#     loop.run_in_executor(None, run)
    
#     # Run the event loop
#     loop.run_until_complete(main_task)