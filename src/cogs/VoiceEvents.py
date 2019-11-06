from discord.ext import commands
from discord import utils

class VoiceEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if before.channel is None and after.channel is not None:
            print(member.name + " just joined a channel!")
            # Get all users subscribed to the channel.
            # For each user subscribed to channel, first check if their whitelist is enabled.
            # If enabled, check if user who joined is in it. If not, don't DM user.
            # If user is whitelisted, send DM.
            # Set a flag called is_notified to indicate user was notified, prevent spam.
            whitelisters = self.bot.db.get_all_subbed_users(str(after.channel.id), str(member.guild.id), str(member.id))
            # Does not work if user doesnt have whitelist. Need to check the user's whitelist first.
            for id in whitelisters:
                user = utils.find(lambda u : u.id == int(id), member.guild.members)
                if user is not None:
                    await user.send('{} has joined {}'.format(member.name, after.channel.name))
        elif before.channel is not None and after.channel is not None:
            print("{} switched from {} to {}".format(member.name, before.channel.name, after.channel.name))
            whitelisters = self.bot.db.get_all_subbed_users(str(after.channel.id), str(member.guild.id), str(member.id))
            
            for id in whitelisters:
                user = utils.find(lambda u : u.id == int(id), member.guild.members)
                if user is not None:
                    await user.send('{} has switched to {} from {}'.format(member.name, after.channel.name, before.channel.name))
        elif before.channel is not None and after.channel is None:
            print("{} left {}".format(member.name, before.channel.name))
            whitelisters = self.bot.db.get_all_subbed_users(str(before.channel.id), str(member.guild.id), str(member.id))
            for id in whitelisters:
                user = utils.find(lambda u : u.id == int(id), member.guild.members)
                if user is not None:
                    await user.send('{} has left {}'.format(member.name, before.channel.name))


        

        
def setup(bot):
    bot.add_cog(VoiceEvents(bot))