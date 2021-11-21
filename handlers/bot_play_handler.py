from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from config import MAX_LIMIT, MIN_LIMIT
from database_schemes import GameLogClass
from keyboards.main_keyboards import choose_answer_keyboard, choose_mode_keyboard, stop_game_keyboard
from loader import dp
from states import playing_person

from handlers.start_handler import delete_keyboard


@dp.callback_query_handler(state=playing_person.bot_is_paying)
async def start_work(call: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    min_limit = data.get("min_limit")
    max_limit = data.get("max_limit")
    previous_attempt = data.get("attempt")
    game_log = GameLogClass.objects(pk=data.get("game_log_id"))

    await delete_keyboard(await state.get_data(), call.from_user.id)
    await state.update_data(previous_keyboard_id=None)

    if call.data == "right":
        await call.message.edit_text(
            text=f"Right: {previous_attempt}\nTo start a new game choose mode",
            reply_markup=choose_mode_keyboard,
        )
        await state.update_data(previous_keyboard_id=call.message.message_id + 1)

        game_log.update_one(
            guessed_num=previous_attempt,
            game_finish_date=datetime.now(),
            is_finished_correctly=True,
        )

        await state.finish()

    else:
        await call.message.edit_text(
            text=f"My number is {call.data} than {previous_attempt}"
        )
        if call.data == "higher":
            new_attempt = (previous_attempt + max_limit) // 2
            await state.update_data(min_limit=previous_attempt)
            min_limit = previous_attempt
        elif call.data == "lower":
            new_attempt = (min_limit + previous_attempt) // 2
            await state.update_data(max_limit=previous_attempt)
            max_limit = previous_attempt

        await state.update_data(attempt=new_attempt)

        if max_limit - min_limit <= 1:
            max_limit = MAX_LIMIT if max_limit == MAX_LIMIT + 1 else max_limit
            min_limit = MIN_LIMIT if min_limit == MIN_LIMIT - 1 else min_limit
            game_log.update_one(
                game_finish_date=datetime.now(),
                is_finished_correctly=False,
            )
            await call.message.answer(
                text=f"Your data is incorrect\nnumber can't be higher than {min_limit} and lower than {max_limit}\nTo start a new game choose mode",
                reply_markup=choose_mode_keyboard,
            )
            await state.update_data(previous_keyboard_id=call.message.message_id + 1)

            await state.finish()
        else:
            game_log.update_one(
                attempts_num=game_log[0].attempts_num + 1,
            )

            await call.message.answer(
                text=str(new_attempt), reply_markup=choose_answer_keyboard
            )


@dp.message_handler(state=playing_person.bot_is_paying)
async def start_work(message: Message, state: FSMContext):

    await delete_keyboard(await state.get_data(), message.from_user.id)
    await state.update_data(previous_keyboard_id=message.message_id + 1)

    await message.answer(
        text="Use buttons above\nor you can stop this game",
        reply_markup=stop_game_keyboard,
    )
