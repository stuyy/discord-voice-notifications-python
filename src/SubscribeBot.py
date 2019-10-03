import discord
from discord.ext import commands

class SubscribeBot(commands.Bot):

    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        
    async def on_ready(self):
        print("Ready")