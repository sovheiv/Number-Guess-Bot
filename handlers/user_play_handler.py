from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from database_schemes import GameLogCollection
from loader import keyboard_logger
from keyboards.main_keyboards import choose_mode_keyboard, stop_game_keyboard
from loader import dp
from states import playing_person

from handlers.start_handler import delete_keyboard


@dp.message_handler(state=playing_person.user_is_paying)
async def proces_user_play(message: types.Message, state: FSMContext):

    data = await state.get_data()

    number = data.get("number")

    game_log = GameLogCollection.objects(pk=data.get("game_log_id"))

    await delete_keyboard(data, message.from_user.id)
    await state.update_data(previous_keyboard_id=None)

    if not message.text.isdigit():

        await message.answer(
            text="Not number error\n you should write numbers or you can stop this game",
            reply_markup=stop_game_keyboard,
        )

        await state.update_data(previous_keyboard_id=message.message_id + 1)
        keyboard_logger.debug(f"{message.from_user.id} Created: {message.message_id + 1}")

        return

    answer = int(message.text)
    game_log.update_one(
        attempts_num=game_log[0].attempts_num + 1,
    )

    attempts_num = game_log[0].attempts_num

    if answer == number:
        await message.answer(
            text=f"You have guessed the number!\nAttempts: {attempts_num}\nTo start a new game choose mode:",
            reply_markup=choose_mode_keyboard,
        )
        game_log.update_one(game_finish_date=datetime.now(), is_finished_correctly=True)
        keyboard_logger.debug(f"{message.from_user.id} Created: {message.message_id + 1}")

        await state.update_data(number=None)
        await state.finish()
        await state.update_data(previous_keyboard_id=message.message_id + 1)

        return

    elif answer > number:
        comparsion = "lower"

    elif answer < number:
        comparsion = "higher"

    await message.answer(text=f"Bot's number is {comparsion} than {message.text} \nAttempts: {attempts_num}")

    await state.update_data(attempts=attempts_num + 1)
