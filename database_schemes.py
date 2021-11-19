from datetime import datetime

import mongoengine
from mongoengine import fields

mongoengine.connect(db="guess-the-number-bot-database", host="127.0.0.1", port=27017)


class UsersClass(mongoengine.Document):
    user_id = fields.IntField(unique=True)
    first_name = fields.StringField()
    username = fields.StringField()
    language_code = fields.StringField()
    date_of_first_contact = fields.DateTimeField(default=datetime.now())
    date_of_last_contact = fields.DateTimeField(default=datetime.now())
    actions_num = fields.IntField(default=1)
    is_banned = fields.BooleanField(default=False)


class GameLogClass(mongoengine.Document):
    user_id = fields.IntField()
    username = fields.StringField()
    game_type = fields.StringField()
    guessed_num = fields.IntField()
    attempts_num = fields.IntField()
    game_start_date = fields.DateTimeField(default=datetime.now())
    game_finish_date = fields.DateTimeField()
    is_finished_correctly = fields.BooleanField()
