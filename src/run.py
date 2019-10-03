from dotenv import load_dotenv
from discord.ext import commands
from SubscribeBot import SubscribeBot
from database import Database
import os

load_dotenv()

db = Database()

client = SubscribeBot(db, command_prefix='?', case_insensitive=True)
exts = ['cogs.Subscribe', 'cogs.Whitelist']

if __name__ == '__main__':
    for ext in exts:
        client.load_extension(ext)
print(os.getenv("YEET"))
client.run(os.getenv("TOKEN"))