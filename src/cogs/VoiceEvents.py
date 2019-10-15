from discord.ext import commands

class VoiceEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        if before.channel is None and after.channel is not None:
            print(member.name + " just joined a channel!")
        elif before.channel is not None and after.channel is not None:
            print("{} switched from {} to {}".format(member.name, before.channel.name, after.channel.name))
        elif before.channel is not None and after.channel is None:
            print("{} left {}".format(member.name, before.channel.name))
        
def setup(bot):
    bot.add_cog(VoiceEvents(bot))