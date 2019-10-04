from discord.ext import commands
import discord
import re

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['wl'], invoke_without_command=True)
    async def whitelist(self, ctx):
        whitelist = self.bot.db.get_user_whitelist(ctx)
        print(whitelist)
        if bool(whitelist):
            print(whitelist)
        else:
            print('empty')
        
    @whitelist.command(name='add', aliases=['a'])
    async def whitelist_add(self, ctx, channel, *args):
        # self.db.add_wl(ctx)
        try:
            voice_channel = discord.utils.find(lambda c: c.id == int(channel), ctx.guild.voice_channels)
            if voice_channel is not None:
                whitelist = self.parse_users(ctx, voice_channel, args)
                if whitelist is not None:
                    self.bot.db.whitelist_add(ctx, voice_channel.id, whitelist)
            else:
                print('no voice channel found')

        except Exception as error:
            voice_channel = discord.utils.find(lambda c : c.name == channel, ctx.guild.voice_channels)
            if voice_channel is not None:
                whitelist = self.parse_users(ctx, voice_channel, args)
                if whitelist is not None:
                    self.bot.db.whitelist_add(ctx, voice_channel.id, whitelist)
            else:
                print('no voice channel foundd')


    @whitelist.command(name='remove', aliases=['r', 'rm'])
    async def whitelist_remove(self, ctx):
        print('remove')
    
    @commands.command(name='clearwl')
    async def clear_wl(self, ctx):
        pass

    @whitelist.command(name='enable')
    async def whitelist_enable(self, ctx):
        print("Enabling whitelist.")
    
    @whitelist.command(name='disable')
    async def whitelist_disable(self, ctx):
        print("Disabling whitelist.")

    def parse_users(self, ctx, channel, args):
        mentioned_users = ctx.message.mentions
        channel_id = str(channel.id)
        user_whitelist = {
            channel_id : []
        }
        for arg in args:
            try:
                id = re.search("\d+", arg).group(0)
                member = discord.utils.find(lambda m : m.id == int(id), ctx.guild.members)
                if member is not None:
                    if member.id == ctx.author.id or member.bot:
                        raise Exception("Cannot whitelist yourself/bot")
                    else:
                        user_whitelist[channel_id].append(member.id)
            except Exception as error:
                print(error)
        
        return user_whitelist if len(user_whitelist[channel_id]) != 0 else None

def setup(bot):
    bot.add_cog(Whitelist(bot))