from discord.ext import commands
import discord
from util.util import *

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['sub', 's'], invoke_without_command=True, case_insensitive=True)
    async def subscribe(self, ctx, *args):
        valid_voice_channels =  parse_channels(ctx, args)
        print(valid_voice_channels)
        # Append to Database.
        self.bot.db.subscribe(valid_voice_channels, ctx)
    
    @commands.group(aliases=['unsub'], invoke_without_command=True)
    async def unsubscribe(self, ctx, *args):
        valid_voice_channels = parse_channels(ctx, args)
        self.bot.db.unsubscribe(valid_voice_channels, ctx)

    @commands.command()
    async def subbed(self, ctx):
        channels = self.bot.db.get_subbed_channels(ctx)
        guild = ctx.guild
        embed=discord.Embed()
        embed.title='Subscribed Channels'
        embed.set_author(name="{}#{}".format(ctx.author.name, ctx.author.discriminator), icon_url=ctx.author.avatar_url)
        if channels is not None:
            vc_list = []
            for channel in channels:
                print(channel)
                res = discord.utils.get(ctx.guild.voice_channels, id=int(channel))
                if res is not None:
                    vc_list.append(res)

            description = ''
            for channel in vc_list:
                embed.add_field(name='**{} Channel**'.format(channel.name), value=channel.id, inline=False)
            
            embed.description=description
            embed.color=1733275
            await ctx.channel.send(embed=embed)
    
    @subscribe.command(name='all')
    async def sub_all(self, ctx):
        print('sub all')

    @unsubscribe.command(name='all')
    async def unsub_all(self, ctx):
        print('unsub all')

def setup(bot):
    bot.add_cog(Subscribe(bot))