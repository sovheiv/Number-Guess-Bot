from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from database_schemes import GameLogClass
from keyboards.main_keyboards import choose_mode_keyboard, stop_game_keyboard
from loader import bot, dp
from states import playing_person


@dp.message_handler(state=playing_person.user_is_paying)
async def start_work(message: types.Message, state: FSMContext):
    data = await state.get_data()

    number = data.get("number")

    game_log = GameLogClass.objects(pk=data.get("game_log_id"))

    if data.get("previous_keyboard_id"):
        await bot.edit_message_reply_markup(
            chat_id=message.from_user.id,
            message_id=data.get("previous_keyboard_id"),
            reply_markup=None,
        )
        await state.update_data(previous_keyboard_id=None)

    if message.text.isdigit():
        answer = int(message.text)
        game_log.update_one(
            attempts_num=game_log[0].attempts_num + 1,
        )

        attempts_num = game_log[0].attempts_num

        if answer > number:
            await message.answer(
                text="Bot's number is lower than "
                + str(message.text)
                + "\nAttempts: "
                + str(attempts_num)
            )

        elif answer < number:
            await message.answer(
                text="Bot's number is higher than "
                + str(message.text)
                + "\nAttempts: "
                + str(attempts_num)
            )

        elif answer == number:
            await message.answer(
                text=f"You have guessed the number!\nAttempts: {attempts_num}\nTo start a new game choose mode:",
                reply_markup=choose_mode_keyboard,
            )
            game_log.update_one(
                game_finish_date=datetime.now(), is_finished_correctly=True
            )

            await state.update_data(number=None)
            await state.finish()
        await state.update_data(attempts=attempts_num + 1)

    else:
        await message.answer(
            text="Not number error\n you should write numbers or you can stop this game",
            reply_markup=stop_game_keyboard,
        )
        await state.update_data(previous_keyboard_id=message.message_id + 1)
