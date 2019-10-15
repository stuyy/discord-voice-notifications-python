from mongoengine import *
import datetime


'''
user_id - The id of user
username - Username of the user
subbed_channels - A Dictionary of guilds that map to the subscribed channels a user is in.
'''
class GuildMember(Document):
    user_id = StringField(primary_key=True, required=True)
    username = StringField(required=True)
    # guilds = DictField(required=False)
    channels = DictField(required=False)

class GuildMemberWhitelist(Document):
    whitelist_id = DictField(primary_key=True, required=True)
    whitelist = DictField(required=False) # Dictionary of Channel IDs mapping to a list of user ids that are whitelisted.
    whitelist_enabled = BooleanField(default=True)

class VoiceChannel(Document):
    id = DictField(primary_key=True, required=True)
    subscribed_users = DictField(required=False)
    #limited = BooleanField(required=False, default=False) # If true, subscribable_users must be checked.
    #subscribable_users = ListField(required=False)

class VoiceChannelWhitelist(Document):
    id = DictField(primary_key=True, required=True) #  Guild ID, VoiceChannel ID, User ID
    enabled = BooleanField(default=False)
    whitelisters = ListField(default=[])
    whitelist = ListField(default=[])