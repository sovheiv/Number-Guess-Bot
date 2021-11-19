from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types
from database_schemes import UsersClass
from datetime import datetime
import mongoengine


class ControlUpdate(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        # print("_____________update_____________")
        # print(update)
        if update.callback_query:
            try:
                user = UsersClass(
                    user_id=update.callback_query.from_user.id,
                    first_name=update.callback_query.from_user.first_name,
                    username=update.callback_query.from_user.username,
                    language_code=update.callback_query.from_user.language_code,
                )
                user.save()
            except mongoengine.errors.NotUniqueError:
                user = UsersClass.objects(user_id=update.callback_query.from_user.id)
                user.update_one(
                    first_name=update.callback_query.from_user.first_name,
                    username=update.callback_query.from_user.username,
                    language_code=update.callback_query.from_user.language_code,
                    date_of_last_contact=datetime.now(),
                    actions_num=user[0].actions_num + 1,
                )
                check_user_ban(user[0])

        elif update.message:
            try:
                user = UsersClass(
                    user_id=update.message.from_user.id,
                    first_name=update.message.from_user.first_name,
                    username=update.message.from_user.username,
                    language_code=update.message.from_user.language_code,
                )
                user.save()
            except mongoengine.errors.NotUniqueError:
                user = UsersClass.objects(user_id=update.message.from_user.id)
                user.update_one(
                    first_name=update.message.from_user.first_name,
                    username=update.message.from_user.username,
                    language_code=update.message.from_user.language_code,
                    date_of_last_contact=datetime.now(),
                    actions_num=user[0].actions_num + 1,
                )
                check_user_ban(user[0])

def check_user_ban(user: dict):
    if user["is_banned"] == True:
        print("banned user tried to write")
        raise CancelHandler()

