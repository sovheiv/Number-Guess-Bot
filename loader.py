import logging
import os
from logging import FileHandler, Formatter, StreamHandler

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


aiogram_logger = logging.getLogger("aiogram")
aiogram_logger.setLevel(logging.INFO)

os.makedirs("logs", exist_ok=True)

aiogram_file_handler = FileHandler(filename="logs/aiogram.log")
aiogram_file_handler.setLevel(logging.DEBUG)
aiogram_file_handler.setFormatter(
    Formatter("{filename} [LINE:{lineno}] #{levelname} [{asctime}]  {message}", style="{")
)

aiogram_console_handler = StreamHandler()
aiogram_console_handler.setLevel(logging.DEBUG)
aiogram_console_handler.setFormatter(
    Formatter("{filename} [LINE:{lineno}] #{levelname} [{asctime}]  {message}", style="{")
)

aiogram_logger.addHandler(aiogram_file_handler)
aiogram_logger.addHandler(aiogram_console_handler)
