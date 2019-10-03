from discord.ext import commands
import discord
class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['sub', 's'], invoke_without_command=True, case_insensitive=True)
    async def subscribe(self, ctx, *args):

        guild = discord.utils.find(lambda g : g.id == int(ctx.guild.id), self.bot.guilds)

        if guild is not None:
            valid_voice_channels = {} # List of all IDs to subscribe user to.
            for arg in args:
                # Find by ID first, if not found, find by name.
                try:
                    ch = discord.utils.find(lambda c : c.id == int(arg), guild.voice_channels)
                    if ch is not None:
                        if str(ch.id) in valid_voice_channels:
                            pass
                        else:
                            valid_voice_channels[ch.id] = ch

                except Exception as error:
                    print(error)
                    ch = discord.utils.find(lambda c : c.name == arg, guild.voice_channels)
                    if ch is not None:
                        if str(ch.id) in valid_voice_channels:
                            pass
                        else:
                            valid_voice_channels[str(ch.id)] = ch

            
        else:
            print('Invalid.')

    
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