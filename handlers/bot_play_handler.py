from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from keyboards.main_keyboards import (
    choose_answer_keyboard,
    choose_mode_keyboard,
    stop_game_keyboard,
)
from loader import dp
from states import paying_person


@dp.callback_query_handler(state=paying_person.bot_is_paying)
async def start_work(call: CallbackQuery, state: FSMContext):
    print(call.data)

    data = await state.get_data()
    min_limit = data.get("min_limit")
    max_limit = data.get("max_limit")
    previous_attempt = data.get("attempt")

    await call.message.edit_text(
        text=f"My number is {call.data} than {previous_attempt}"
    )

    if max_limit - min_limit <= 1:
        await call.message.answer(
            text=f"your data is incorrect\nnumber can`t be higher than {max_limit} and lower than {min_limit}\nTo start a new game choose mode",
            reply_markup=choose_mode_keyboard,
        )
        await state.finish()

    elif call.data == "right":
        await call.message.edit_text(
            text=f"Right: {previous_attempt}\nTo start a new game choose mode",
            reply_markup=choose_mode_keyboard,
        )
        await state.finish()

    else:
        if call.data == "higher":
            new_attempt = (previous_attempt + max_limit) // 2
            await state.update_data(min_limit=previous_attempt)
        elif call.data == "lower":
            new_attempt = (min_limit + previous_attempt) // 2
            await state.update_data(max_limit=previous_attempt)

        await state.update_data(attempt=new_attempt)

        await call.message.answer(
            text=str(new_attempt), reply_markup=choose_answer_keyboard
        )


@dp.message_handler(state=paying_person.bot_is_paying)
async def start_work(message: Message, state: FSMContext):
    await message.answer(
        text="Use buttons above\nor you can stop this game",
        reply_markup=stop_game_keyboard,
    )
    await state.update_data(previous_keyboard_id=message.message_id + 1)
