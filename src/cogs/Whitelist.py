from discord.ext import commands

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['wl'], invoke_without_command=True)
    async def whitelist(self, ctx):
        print('yo')

    @whitelist.command(name='show', aliases=['display'])
    async def whitelist_show(self, ctx):
        print('show')

    @whitelist.command(name='add', aliases=['a'])
    async def whitelist_add(self, ctx):
        print('add')

    @whitelist.command(name='remove', aliases=['r', 'rm'])
    async def whitelist_remove(self, ctx):
        print('remove')
    
    @commands.command(name='clearwl')
    async def clear_wl(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Whitelist(bot))