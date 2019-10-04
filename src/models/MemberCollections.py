from mongoengine import *
import datetime

class GuildMember(Document):
    user_id = StringField(primary_key=True, required=True)
    username = StringField(required=True)
    guilds = DictField(required=False)
    channels = DictField(required=False)
    whitelist = DictField(required=False) # Dictionary of Channel IDs mapping to a list of user ids that are whitelisted.
    whitelist_enabled = BooleanField(default=False)

