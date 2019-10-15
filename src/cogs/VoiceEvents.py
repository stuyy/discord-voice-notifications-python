from discord.ext import commands

class VoiceEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print(member.name)

    
def setup(bot):
    bot.add_cog(VoiceEvents(bot))