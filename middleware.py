from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types
from database_schemes import UsersCollection
from datetime import datetime
import mongoengine


class ControlUpdate(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        # print("_____________update_____________")
        # print(update)
        if update.callback_query:
            check_user_data(update.callback_query)

        elif update.message:
            check_user_data(update.message)

def check_user_data(main_data):
    try:
        user = UsersCollection(
            user_id=main_data.from_user.id,
            first_name=main_data.from_user.first_name,
            username=main_data.from_user.username,
            language_code=main_data.from_user.language_code,
        )
        user.save()
    except mongoengine.errors.NotUniqueError:
        user = UsersCollection.objects(user_id=main_data.from_user.id)
        user.update_one(
            first_name=main_data.from_user.first_name,
            username=main_data.from_user.username,
            language_code=main_data.from_user.language_code,
            date_of_last_contact=datetime.now(),
            actions_num=user[0].actions_num + 1,
        )
        check_user_ban(user[0])

def check_user_ban(user: dict):
    if user["is_banned"] == True:
        print("banned user tried to write")
        raise CancelHandler()
