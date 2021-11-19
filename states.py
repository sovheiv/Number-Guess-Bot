from aiogram.dispatcher.filters.state import State, StatesGroup


class paying_person(StatesGroup):
    bot_is_paying = State()
    user_is_paying = State()
