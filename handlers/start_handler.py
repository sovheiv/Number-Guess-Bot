import inspect
import random
from datetime import datetime

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery
from config import MAX_LIMIT, MIN_LIMIT
from database_schemes import GameLogCollection
from loader import keyboard_logger
from keyboards.main_keyboards import choose_mode_keyboard, create_choose_answer_keyboard
from loader import bot, dp
from states import playing_person


@dp.callback_query_handler(text="user_play")
async def start_user_play_game(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text=f"mode: user play\nBot thought the number from {MIN_LIMIT} to {MAX_LIMIT}\nGuess it"
    )

    data = await state.get_data()
    keyboard_logger.debug(f"{call.from_user.id} Edited without keyboard: {data.get('previous_keyboard_id')}")
    await state.update_data(previous_keyboard_id=None)

    await call.answer("generated")
    rand_number = random.randrange(MAX_LIMIT)

    game_log = GameLogCollection(
        user_id=call.from_user.id,
        username=call.from_user.username,
        game_type=call.data,
        guessed_num=rand_number,
        game_start_date=datetime.now(),
    )
    game_log.save()

    await state.update_data(game_log_id=game_log.pk)
    await state.update_data(number=rand_number)
    await playing_person.user_is_paying.set()


@dp.callback_query_handler(text="bot_play")
async def start_bot_play_game(call: CallbackQuery, state: FSMContext):

    await call.message.edit_text(text="mode: bot play")

    data = await state.get_data()
    keyboard_logger.debug(f"{call.from_user.id} Edited without keyboard: {data.get('previous_keyboard_id')}")
    await state.update_data(previous_keyboard_id=None)

    await call.answer("guess your number")
    await call.message.answer(
        text=f"Think of a number from {MIN_LIMIT} to {MAX_LIMIT}.\nBot will guess your number within 7 tries"
    )

    game_log = GameLogCollection(
        user_id=call.from_user.id,
        username=call.from_user.username,
        game_type=call.data,
        game_start_date=datetime.now(),
    )
    game_log.save()

    await state.update_data(game_log_id=game_log.pk)

    await state.update_data(max_limit=MAX_LIMIT + 1)
    await state.update_data(min_limit=MIN_LIMIT - 1)
    await playing_person.bot_is_paying.set()

    attempt = (MIN_LIMIT + MAX_LIMIT) // 2
    await state.update_data(attempt=attempt)

    await call.message.answer(
        text=f"Is your number {attempt}?", reply_markup=await create_choose_answer_keyboard(attempt)
    )

    await state.update_data(previous_keyboard_id=call.message.message_id + 2)
    keyboard_logger.debug(f"{call.from_user.id} Created: {call.message.message_id + 2}")


@dp.message_handler(commands="info_about_current_mode", state="*")
async def process_info_about_current_mode(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "playing_person:user_is_paying":
        await message.answer(
            text="In this mode you should try to guess the number wich this bot though of\nWrite the bot some number, for example, 50",
        )
    elif current_state == "playing_person:bot_is_paying":
        data = await state.get_data()
        attempt = data.get("attempt")
        await delete_keyboard(data, message.from_user.id)
        await message.answer(
            text=(
                "In this mode you should think of a number and bot will guess it within 7 tries\n\n"
                f"<b>Press buttons above</b> to set is your number higher or lower than {attempt}. Or is it {attempt}?"
            ),
            reply_markup=await create_choose_answer_keyboard(attempt),
        )
        await state.update_data(previous_keyboard_id=message.message_id + 1)
        keyboard_logger.debug(f"{message.from_user.id} Created: {message.message_id + 1}")
    elif not current_state:

        await delete_keyboard(await state.get_data(), message.from_user.id)

        await message.answer(
            text=(
                "Now you haven't any active games.\nTo start a new game choose mode:\n\n"
                "• <b>User play</b> – is the mode in which bot think of a number and you can guess it\n\n"
                "• <b>Bot play</b> – is the mode in which you can think of a number. After that  bot will guess it within 7 tries"
            ),
            reply_markup=choose_mode_keyboard,
        )
        await state.update_data(previous_keyboard_id=message.message_id + 1)
        keyboard_logger.debug(f"{message.from_user.id} Created: {message.message_id + 1}")


@dp.message_handler(state="*", commands="stop_game")
async def process_stop_game_command(message: types.Message, state: FSMContext):
    await stop_game(message, state)


@dp.callback_query_handler(state="*", text="stop_game")
async def process_stop_game_callback(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    keyboard_logger.debug(f"{call.from_user.id} Edited without keyboard: {data.get('previous_keyboard_id')}")
    await state.update_data(previous_keyboard_id=None)
    await stop_game(call.message, state)


async def stop_game(message, state: FSMContext):

    await delete_keyboard(await state.get_data(), message.from_user.id)

    await message.answer(
        text="Stoped.\nTo start a new game choose mode:",
        reply_markup=choose_mode_keyboard,
    )
    keyboard_logger.debug(f"{message.from_user.id} Created: {message.message_id + 1}")
    data = await state.get_data()
    game_log_id = data.get("game_log_id")

    if game_log_id:
        game_log = GameLogCollection.objects(pk=game_log_id)
        game_log.update_one(game_finish_date=datetime.now(), is_finished_correctly=False)

    await state.finish()
    await state.update_data(previous_keyboard_id=message.message_id + 1)


def log_decorator(func):
    def wrapped_func(*args, **kwargs):
        data = args[0]
        user_id = args[1]
        try:
            result = func(*args, **kwargs)
            keyboard_logger.debug(
                f"real_func: {inspect.stack()[1].function} {user_id} Deleted: {data.get('previous_keyboard_id')}"
            )
            return result
        except aiogram.utils.exceptions.MessageToEditNotFound:
            keyboard_logger.exception(
                f"{user_id} Tried to deleted: {data.get('previous_keyboard_id')}",
                exc_info=True,
            )

    return wrapped_func


@log_decorator
async def delete_keyboard(data, chat_id):
    if data.get("previous_keyboard_id"):
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=data.get("previous_keyboard_id"),
            reply_markup=None,
        )
