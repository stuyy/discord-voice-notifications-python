from discord.ext import commands
import discord
from util.util import *

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['sub', 's'], invoke_without_command=True, case_insensitive=True)
    async def subscribe(self, ctx, *args):
        valid_voice_channels = parse_channels(ctx, args) # This is a Dictionary of the Guild ID mapping to all VC Channels to Subscribe to.
        # Append to Database.
        self.bot.db.subscribe(valid_voice_channels, ctx)
    
    @commands.group(aliases=['unsub'], invoke_without_command=True)
    async def unsubscribe(self, ctx, *args):
        valid_voice_channels = parse_channels(ctx, args)
        guild = ctx.guild
        embed = discord.Embed()
        if len(valid_voice_channels[str(guild.id)]) == 0:
            pass
        else:
            result = self.bot.db.unsubscribe(valid_voice_channels, ctx)
            if result:
                print('Success!')
            else:
                print("nope")
    @commands.command(aliases=['subbed'])
    async def subscribed(self, ctx):
        guild = ctx.guild
        channels = self.bot.db.get_subbed_channels(ctx.author, ctx.guild)
        if channels is None:
            return
        embeds = generate_embeds(channels, guild, ctx.author)

        if len(embeds) != 0:
            msg = await ctx.channel.send(embed=embeds[0])
            await msg.add_reaction('◀')
            await msg.add_reaction('▶')
        else:
            print('no embeds')
        
        '''
        if channels is not None:
            vc_list = []
            for channel in channels:
                res = discord.utils.get(ctx.guild.voice_channels, id=int(channel))
                if res is not None:
                    vc_list.append(res)

            for channel in vc_list:
                embed.add_field(name='**{}**'.format(channel.name), value=channel.id, inline=False)
            
            await ctx.channel.send(embed=embed)
        '''
    @subscribe.command(name='all')
    async def sub_all(self, ctx):
        print('sub all')

    @unsubscribe.command(name='all')
    async def unsub_all(self, ctx):
        print('unsub all')

def setup(bot):
    bot.add_cog(Subscribe(bot))