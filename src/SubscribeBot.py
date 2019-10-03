import discord
from discord.ext import commands

class SubscriberBot(commands.Bot):
    async def on_ready(self):
        print("Ready")
