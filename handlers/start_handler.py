import random
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.callback_data import CallbackData
from config import MAX_LIMIT, MIN_LIMIT
from database_schemes import GameLogClass
from keyboards.main_keyboards import choose_answer_keyboard, choose_mode_keyboard
from loader import dp
from states import playing_person


@dp.callback_query_handler(text="user_play")
async def generate_number(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text=f"mode: user play\nBot thought the number from {MIN_LIMIT} to {MAX_LIMIT}\nGuess it"
    )
    await call.answer("generated")
    rand_number = random.randrange(MAX_LIMIT)

    game_log = GameLogClass(
        user_id=call.from_user.id,
        username=call.from_user.username,
        game_type=call.data,
        guessed_num=rand_number,
        attempts_num=0,
    )
    game_log.save()

    await state.update_data(game_log_id=game_log.pk)
    await state.update_data(number=rand_number)
    await playing_person.user_is_paying.set()


@dp.callback_query_handler(text="bot_play")
async def generate_number(call: CallbackData, state: FSMContext):
    await call.message.edit_text(text="mode: bot play")

    await call.answer("guess your number")
    await call.message.answer(
        text=f"Think of a number from {MIN_LIMIT} to {MAX_LIMIT}\nand remember it.\nBot will guess your number within 7 tries"
    )

    game_log = GameLogClass(
        user_id=call.from_user.id,
        username=call.from_user.username,
        game_type=call.data,
        attempts_num=0,
    )
    game_log.save()

    await state.update_data(game_log_id=game_log.pk)

    await state.update_data(attempt=None)
    await state.update_data(max_limit=MAX_LIMIT + 1)
    await state.update_data(min_limit=MIN_LIMIT - 1)
    await playing_person.bot_is_paying.set()

    data = await state.get_data()

    attempt = (data.get("min_limit") + data.get("max_limit")) // 2
    await state.update_data(attempt=attempt)
    await call.message.answer(text=str(attempt), reply_markup=choose_answer_keyboard)


@dp.message_handler(state="*", commands="stop_game")
async def start_work(message: types.Message, state: FSMContext):
    await stop_game(message, state)


@dp.callback_query_handler(state="*", text="stop_game")
async def generate_number(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await stop_game(call.message, state)


async def stop_game(message, state: FSMContext):
    await message.answer(
        text="Stoped.\nTo start a new game choose mode:",
        reply_markup=choose_mode_keyboard,
    )
    data = await state.get_data()
    game_log = GameLogClass.objects(pk=data.get("game_log_id"))
    game_log.update_one(game_finish_date=datetime.now(), is_finished_correctly=False)
    await state.finish()
