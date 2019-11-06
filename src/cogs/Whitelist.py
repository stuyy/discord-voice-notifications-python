from discord.ext import commands
import discord
import re

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['wl'], invoke_without_command=True)
    async def whitelist(self, ctx):
        embed = discord.Embed()
        embed.set_author(name="{}#{}'s Whitelist".format(ctx.author.name, ctx.author.discriminator), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text='To whitelist someone, first subscribe to a channel, and then issue the command: e.g: ?wl add 582319490604335107 @UserToWhitelist#1337')
        embed.description = ''
        whitelist = self.bot.db.get_user_whitelist(ctx)
        for wl in whitelist:
            vc = discord.utils.find(lambda c: c.id == int(wl.id['vc_id']), ctx.guild.voice_channels)
            if vc is not None:
                field = ''
                for member_id in wl.whitelist:
                    member = discord.utils.find(lambda m : m.id == int(member_id), ctx.guild.members)
                    if member is not None:
                        field += '{} ({})\n'.format(member.name, member.id)
                print(field)
                if len(field) == 0:
                    field = '\u200b'
                embed.add_field(name=vc.name, value=field, inline=False)
        print(embed.fields)
        await ctx.channel.send(embed=embed)
    
    @whitelist.command(name='add', aliases=['a'])
    async def whitelist_add(self, ctx, channel, *args):
        embed = discord.Embed()
        try:
            voice_channel = discord.utils.find(lambda c: c.id == int(channel), ctx.guild.voice_channels)
            if voice_channel is not None:
                whitelist = self.parse_users(ctx, voice_channel, args)
                if whitelist is not None:
                    flag = self.bot.db.whitelist_add(ctx, voice_channel.id, whitelist)
                    if flag == False:
                        embed.description='You are not subscribed to ' + voice_channel.name
                        await ctx.channel.send(embed=embed)
            else:
                print('no voice channel found')

        except Exception as error:
            voice_channel = discord.utils.find(lambda c : c.name == channel, ctx.guild.voice_channels)
            if voice_channel is not None:
                whitelist = self.parse_users(ctx, voice_channel, args)
                if whitelist is not None:
                    flag = self.bot.db.whitelist_add(ctx, voice_channel.id, whitelist)
                    if flag == False:
                        embed.description='You are not subscribed to ' + voice_channel.name
                        await ctx.channel.send(embed=embed)
            else:
                print('no voice channel found')


    @whitelist.command(name='remove', aliases=['r', 'rm'])
    async def whitelist_remove(self, ctx, channel, *args):
        embed = discord.Embed()
        try:
            voice_channel = discord.utils.find(lambda c: c.id == int(channel), ctx.guild.voice_channels)
            if voice_channel is not None:
                whitelist = self.parse_users(ctx, voice_channel, args)
                if whitelist is not None:
                    flag = self.bot.db.whitelist_remove(ctx, voice_channel.id, whitelist)
            else:
                print('no voice channel found')

        except Exception as error:
            voice_channel = discord.utils.find(lambda c : c.name == channel, ctx.guild.voice_channels)
            if voice_channel is not None:
                whitelist = self.parse_users(ctx, voice_channel, args)
                if whitelist is not None:
                    flag = self.bot.db.whitelist_remove(ctx, voice_channel.id, whitelist)
            else:
                print('no voice channel foundd')
    
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
        channel_id = str(channel.id)
        user_whitelist = {
            channel_id : []
        }
        for arg in args:
            try:
                id = re.search("\d+", arg).group(0)
                member = discord.utils.find(lambda m : m.id == int(id), ctx.guild.members)
                if member is not None:
                    if member.id == ctx.author.id:
                        raise Exception("Cannot whitelist yourself/bot")
                    elif str(member.id) in user_whitelist[channel_id]:
                        print("Skipping.")
                    else:
                        user_whitelist[channel_id].append(str(member.id))
            except Exception as error:
                print(error)
        return user_whitelist if len(user_whitelist[channel_id]) != 0 else None

def setup(bot):
    bot.add_cog(Whitelist(bot))