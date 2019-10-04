'''
    Utility Function
'''
import discord
import math
import time

def parse_channels(ctx, args):
    guild = ctx.guild
    if guild is not None: 
        valid_voice_channels = {
            str(guild.id) : []
        } # List of all IDs to subscribe user to.
        for arg in args:
            # Find by ID first, if not found, find by name.
            try:
                ch = discord.utils.find(lambda c : c.id == int(arg), guild.voice_channels)
                if ch is not None:
                    if str(ch.id) in valid_voice_channels[str(guild.id)]: # If key is in dict, pass.
                        pass
                    else:
                        valid_voice_channels[str(guild.id)].append(str(ch.id)) # Add channel id to list.

            except Exception as error:
                ch = discord.utils.find(lambda c : c.name == arg, guild.voice_channels)
                if ch is not None:
                    if str(ch.id) in valid_voice_channels[str(guild.id)]:
                        pass
                    else:
                        valid_voice_channels[str(guild.id)].append(str(ch.id))

        return valid_voice_channels
    
    else:
        return None


def generate_embeds(channels, guild, author):
    # Display 5 at a time.
    max_embeds = math.ceil(len(channels)/5)
    j = 0
    k = 5
    embed_list = []
    for i in range(max_embeds):
        curr_channels = channels[j:k]
        embed=discord.Embed()
        embed.title='Subscribed Channels'
        embed.set_author(name="{}#{}".format(author.name, author.discriminator), icon_url=author.avatar_url)
        embed.color=1733275
        embed.set_footer(text='Current Page: {}/{}'.format(str(int(k/5)), str(max_embeds)))
        for ids in curr_channels:
            channel = discord.utils.find(lambda c : c.id == int(ids), guild.voice_channels)
            if channel is not None:
                # Found Channel.
                embed.add_field(name=channel.name, value=channel.id, inline=False)
        embed_list.append(embed)
        j += 5
        k += 5
    return embed_list
