from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import keyboard_logger
from keyboards.main_keyboards import choose_mode_keyboard
from loader import dp

from handlers.start_handler import delete_keyboard


@dp.message_handler(commands="start")
async def process_start_command(message: types.Message, state: FSMContext):

    await delete_keyboard(await state.get_data(), message.from_user.id)
    await state.update_data(previous_keyboard_id=message.message_id + 1)

    await message.answer(
        text=(
            "That's Guess the number bot.\n\n"
            "To start a new game choose mode:\n\n"
            "• <b>User play</b> – is the mode in which bot think of a number and you can guess it\n\n"
            "• <b>Bot play</b> – is the mode in which you can think of a number. After that  bot will guess it within 7 tries\n\n"
            "To get more information about current game you can choose <code>Info about current mode</code> command in commands list which is left of the input field"
        ),
        reply_markup=choose_mode_keyboard,
    )

    keyboard_logger.debug(f"{message.from_user.id} Created: {message.message_id + 1}")


@dp.message_handler()
async def process_unknown_command(message: types.Message, state: FSMContext):

    await delete_keyboard(await state.get_data(), message.from_user.id)
    await state.update_data(previous_keyboard_id=message.message_id + 1)

    await message.answer(
        text="To start a new game choose mode:", reply_markup=choose_mode_keyboard
    )
    keyboard_logger.debug(f"{message.from_user.id} Created: {message.message_id + 1}")

