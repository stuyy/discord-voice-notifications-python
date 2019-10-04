'''
    Utility Function
'''
import discord
def parse_channels(ctx, args):
    guild = ctx.guild
    print(guild.id)
    if guild is not None:
        valid_voice_channels = {} # List of all IDs to subscribe user to.
        for arg in args:
            # Find by ID first, if not found, find by name.
            try:
                ch = discord.utils.find(lambda c : c.id == int(arg), guild.voice_channels)
                if ch is not None:
                    if str(ch.id) in valid_voice_channels: # If key is in dict, pass.
                        pass
                    else:
                        valid_voice_channels[ch.id] = str(guild.id) # Add key-value pair to dict.

            except Exception as error:
                ch = discord.utils.find(lambda c : c.name == arg, guild.voice_channels)
                if ch is not None:
                    if str(ch.id) in valid_voice_channels:
                        pass
                    else:
                        valid_voice_channels[str(ch.id)] = str(guild.id)

        return valid_voice_channels