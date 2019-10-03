from discord.ext import commands
from SubscribeBot import SubscribeBot
from database import Database
import os

db = Database()

client = SubscribeBot(db, command_prefix='?', case_insensitive=True)
exts = ['cogs.Subscribe', 'cogs.Whitelist']

if __name__ == '__main__':
    for ext in exts:
        client.load_extension(ext)

client.run(os.getenv("TOKEN"))