from aiogram import types
from keyboards.main_keyboards import choose_mode_keyboard
from loader import dp



@dp.message_handler()
async def start_work(message: types.Message):
    await message.answer(
        text="To start a new game choose mode:", reply_markup=choose_mode_keyboard
    )
