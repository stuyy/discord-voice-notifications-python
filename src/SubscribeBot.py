import discord
from discord.ext import commands

class SubscribeBot(commands.Bot):

    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix)

    async def on_ready(self):
        print("Ready")
    
