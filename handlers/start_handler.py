import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from config import max_limit
from keyboards.main_keyboards import choose_answer_keyboard, choose_mode_keyboard
from loader import dp
from states import paying_person


@dp.callback_query_handler(text="user_play")
async def generate_number(call: CallbackData, state: FSMContext):
    await call.message.edit_text(
        text=f"mode: user play\nBot thought the number from 0 to {max_limit}\nGuess it"
    )
    await call.answer("generated")
    rand_number = random.randrange(max_limit)
    print(rand_number)

    await state.update_data(attempts=None)
    await state.update_data(number=rand_number)
    await paying_person.user_is_paying.set()


@dp.callback_query_handler(text="bot_play")
async def generate_number(call: CallbackData, state: FSMContext):
    await call.message.edit_text(text="mode: bot play")

    await call.answer("guess your number")
    await call.message.answer(
        text=f"Think of a number from 0 to {max_limit}\nand remember it.\nBot will guess your number in less than 7 tries"
    )

    await state.update_data(attempt=None)
    await state.update_data(max_limit=max_limit)
    await state.update_data(min_limit=0)
    await paying_person.bot_is_paying.set()

    data = await state.get_data()

    attempt = (data.get("min_limit") + data.get("max_limit")) // 2
    await state.update_data(attempt=attempt)
    await call.message.answer(text=str(attempt), reply_markup=choose_answer_keyboard)


@dp.message_handler(state="*", commands="stop_game")
async def start_work(message: types.Message, state: FSMContext):

    await message.answer(
        text="Stoped.\nTo start a new game choose mode:",
        reply_markup=choose_mode_keyboard,
    )
    await state.finish()


@dp.callback_query_handler(state="*", text="stop_game")
async def generate_number(call: CallbackData, state: FSMContext):
    await call.message.edit_text(
        text="Stoped.\nTo start a new game choose mode:",
        reply_markup=choose_mode_keyboard,
    )
    await state.finish()
