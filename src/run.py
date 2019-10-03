from discord.ext import commands
from SubscribeBot import SubscribeBot
import os

client = SubscribeBot(command_prefix='?')

exts = ['cogs.Subscribe', 'cogs.Whitelist']

if __name__ == '__main__':
    for ext in exts:
        client.load_extension(ext)

client.run(os.getenv("TOKEN"))