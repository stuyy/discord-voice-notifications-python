from discord.ext import commands

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def subscribe(self, ctx):
        print('hi')

    @commands.command()
def setup(bot):
    bot.add_cog(Subscribe(bot))