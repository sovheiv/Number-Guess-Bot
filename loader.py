import logging
import logging.config
import os

import yaml
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

os.makedirs("logs", exist_ok=True)


with open('./logger_config.yaml', 'r') as stream:
    loggers_config = yaml.load(stream, Loader=yaml.FullLoader)


logging.config.dictConfig(loggers_config)

aiogram_logger = logging.getLogger(name="aiogram")
update_logger = logging.getLogger(name="update_logger")
keyboard_logger = logging.getLogger(name="keyboard_logger")
