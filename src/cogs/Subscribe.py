from discord.ext import commands

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['sub', 's'], invoke_without_command=True)
    async def subscribe(self, ctx):
        print('subscribing')

    @commands.group(aliases=['unsub'], invoke_without_command=True)
    async def unsubscribe(self, ctx):
        print('unsub')

    @commands.command()
    async def subbed(self, ctx):
        print('display subbed')

    @subscribe.command(name='all')
    async def sub_all(self, ctx):
        print('sub all')

    @unsubscribe.command(name='all')
    async def unsub_all(self, ctx):
        print('unsub all')


def setup(bot):
    bot.add_cog(Subscribe(bot))