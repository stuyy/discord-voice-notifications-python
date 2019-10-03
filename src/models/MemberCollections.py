from mongoengine import *
import datetime

class GuildMember(Document):
    user_id = StringField(primary_key=True, required=True)
    username = StringField(required=True)
    guilds = DictField(required=False)
    channels = DictField(required=False)
