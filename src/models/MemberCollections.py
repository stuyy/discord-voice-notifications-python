from mongoengine import *
import datetime

class GuildMember(Document):
    user_id = StringField()
    username = StringField()
    guilds = DictField()
    channels = DictField()
