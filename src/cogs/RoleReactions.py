import discord
from discord.ext import commands
from util.util import *
import re
class RoleReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        
        if str(reaction.emoji) == '◀' or str(reaction.emoji) == '▶':
            channels = self.bot.db.get_subbed_channels(user, reaction.message.guild)
            if channels is None:
                return
            
            embed_list = generate_embeds(channels, reaction.message.guild, user)
            current_embed = discord.utils.find(lambda e: e.title == 'Subscribed Channels', reaction.message.embeds)
            result = re.search('\d+', current_embed.footer.text)

            curr_page = int(result.group(0))-1 if result is not None else None
            if str(reaction.emoji) == '◀':
                prev_page = curr_page - 1
                if curr_page < 1:
                    await reaction.message.remove_reaction('▶', user)
                else:
                    await reaction.message.edit(embed=embed_list[prev_page])
                    await reaction.message.remove_reaction('◀', user)

            elif str(reaction.emoji) == '▶':
                next_page = curr_page + 1
                if (next_page+1) > len(embed_list):
                    pass
                else:
                    await reaction.message.edit(embed=embed_list[next_page])
                    await reaction.message.remove_reaction('▶', user)

        

        
def setup(bot):
    bot.add_cog(RoleReaction(bot))