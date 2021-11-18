from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choose_mode_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="user play", callback_data="user_play"),
            InlineKeyboardButton(text="bot play", callback_data="bot_play"),
        ]
    ]
)
choose_answer_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="My number is higher", callback_data="higher")],
        [InlineKeyboardButton(text="Right! It is my number", callback_data="right")],
        [InlineKeyboardButton(text="My number is lower", callback_data="lower")],
    ]
)
stop_game_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="stop game", callback_data="stop_game")]
    ]
)
