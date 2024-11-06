import logging

# configure bot logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log"
)

# instance
bot_logger = logging.getLogger("bot_logger")
bot_logger.addHandler(logging.FileHandler('bot.log'))