from config import ADMIN_ID
from loader import bot, dp, storage


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


async def on_startap(dp):
    await bot.send_message(chat_id=ADMIN_ID, text="bot started, /start")


if __name__ == "__main__":
    from aiogram import executor

    from handlers import dp

    executor.start_polling(dp, on_startup=on_startap, on_shutdown=on_shutdown)
