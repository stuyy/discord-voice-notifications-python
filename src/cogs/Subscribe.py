from discord.ext import commands
import discord
from util.util import *

class Subscribe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['sub', 's'], invoke_without_command=True, case_insensitive=True)
    async def subscribe(self, ctx, *args):
        valid_voice_channels = parse_channels(ctx, args)
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
        channels = self.bot.db.get_subbed_channels(ctx)
        embeds = generate_embeds(channels, ctx)

        msg = await ctx.channel.send(embed=embeds[0])

        def check(reaction, user):
            print(user == msg.author and str(reaction.emoji) == '▶')
            return user == ctx.author and str(reaction.emoji) == '▶'

        await msg.add_reaction('▶')
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