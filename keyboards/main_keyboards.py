from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choose_mode_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="User play", callback_data="user_play"),
            InlineKeyboardButton(text="Bot play", callback_data="bot_play"),
        ]
    ]
)


async def create_choose_answer_keyboard(current_attempt):
    choose_answer_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"My number is higher than {current_attempt}", callback_data="higher")],
            [InlineKeyboardButton(text=f"Right! {current_attempt} is my number", callback_data="right")],
            [InlineKeyboardButton(text=f"My number is lower than {current_attempt}", callback_data="lower")],
        ]
    )
    return choose_answer_keyboard


async def create_choose_answer_and_stop_keyboard(current_attempt):
    choose_answer_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"My number is higher than {current_attempt}", callback_data="higher")],
            [InlineKeyboardButton(text=f"Right! {current_attempt} is my number", callback_data="right")],
            [InlineKeyboardButton(text=f"My number is lower than {current_attempt}", callback_data="lower")],
            [InlineKeyboardButton(text="stop game", callback_data="stop_game")],
        ]
    )
    return choose_answer_keyboard


stop_game_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="stop game", callback_data="stop_game")]]
)
