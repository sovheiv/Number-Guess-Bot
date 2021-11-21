import random
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.callback_data import CallbackData
from config import MAX_LIMIT, MIN_LIMIT
from database_schemes import GameLogClass
from keyboards.main_keyboards import choose_answer_keyboard, choose_mode_keyboard
from loader import bot, dp
from states import playing_person


@dp.callback_query_handler(text="user_play")
async def generate_number(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text=f"mode: user play\nBot thought the number from {MIN_LIMIT} to {MAX_LIMIT}\nGuess it"
    )

    await state.update_data(previous_keyboard_id=None)

    await call.answer("generated")
    rand_number = random.randrange(MAX_LIMIT)

    game_log = GameLogClass(
        user_id=call.from_user.id,
        username=call.from_user.username,
        game_type=call.data,
        guessed_num=rand_number,
        attempts_num=0,
        game_start_date=datetime.now(),
    )
    game_log.save()

    await state.update_data(game_log_id=game_log.pk)
    await state.update_data(number=rand_number)
    await playing_person.user_is_paying.set()


@dp.callback_query_handler(text="bot_play")
async def generate_number(call: CallbackData, state: FSMContext):

    await call.message.edit_text(text="mode: bot play")
    await state.update_data(previous_keyboard_id=None)

    await call.answer("guess your number")
    await call.message.answer(
        text=f"Think of a number from {MIN_LIMIT} to {MAX_LIMIT}.\nBot will guess your number within 7 tries"
    )

    game_log = GameLogClass(
        user_id=call.from_user.id,
        username=call.from_user.username,
        game_type=call.data,
        attempts_num=0,
        game_start_date=datetime.now(),
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


@dp.message_handler(commands="info_about_current_mode", state="*")
async def start_work(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "playing_person:user_is_paying":
        await message.answer(
            text="In this mode you should try to guess the number wich this bot though of\nWrite the bot some number, for example, 50",
        )
    elif current_state == "playing_person:bot_is_paying":
        data = await state.get_data()
        attempt = data.get("attempt")
        await message.answer(
            text=(
                "In this mode you should think of a number and bot will guess it within 7 tries\n\n"
                f"<b>Press buttons above</b> to set is your number higher or lower than {attempt}. Or is it {attempt}?"
            ),
        )
    elif not current_state:

        await delete_keyboard(await state.get_data(), message.from_user.id)
        await state.update_data(previous_keyboard_id=message.message_id + 1)

        await message.answer(
            text=(
                "Now you haven't any active games.\nTo start a new game choose mode:\n\n"
                "• <b>User play</b> – is the mode in which bot think of a number and you can guess it\n\n"
                "• <b>Bot play</b> – is the mode in which you can think of a number. After that  bot will guess it within 7 tries"
            ),
            reply_markup=choose_mode_keyboard,
        )


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
    await state.update_data(previous_keyboard_id=message.message_id + 1)

    data = await state.get_data()
    game_log = GameLogClass.objects(pk=data.get("game_log_id"))
    game_log.update_one(game_finish_date=datetime.now(), is_finished_correctly=False)
    await state.finish()


async def delete_keyboard(data, chat_id):
    if data.get("previous_keyboard_id"):
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=data.get("previous_keyboard_id"),
            reply_markup=None,
        )
