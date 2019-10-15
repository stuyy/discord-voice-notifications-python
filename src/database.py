from mongoengine import connect
from models.MemberCollections import *

class Database:
    def __init__(self, name='subscriberbot'):
        self.connect_db(name)

    def connect_db(self, name):
        connect(name)
        
    def subscribe(self, channels, ctx):
        for id in channels[str(ctx.guild.id)]:
            vc_doc = self.get_vc_document(id)
            if vc_doc is None:
                VoiceChannel(id=id, subscribed_users={ str(ctx.author.id) : [] }, limited=False, subscribable_users=[]).save()
            else:
                subbed = vc_doc.subscribed_users
                if str(ctx.author.id) not in subbed:
                    subbed.append(str(ctx.author.id))
                else:
                    print("Already exists.")
        '''
        member = ctx.author
        query = GuildMember.objects(user_id=str(member.id))
        if len(query) == 0:
            member_doc = GuildMember(str(member.id), str(member.name), channels)
            member_doc.save()
        else:
            member_doc = query[0]
            # Check if key exists in member_doc.channels
            if str(ctx.guild.id) in member_doc.channels:
                member_doc.channels[str(ctx.guild.id)] = list(set(channels[str(ctx.guild.id)]).union(set(member_doc.channels[str(ctx.guild.id)])))
                member_doc.update(set__channels=member_doc.channels)
            else:
                member_doc.channels.update(channels)
                member_doc.update(set__channels=member_doc.channels)
        '''
    def unsubscribe(self, channels, ctx):
        member = ctx.author
        guild = ctx.guild
        # Get the member document first.
        member_doc = self.get_member_document(member.id)
        if member_doc is not None:
            member_doc.channels
            if str(guild.id) in member_doc.channels:
                diff = list(set(member_doc.channels[str(guild.id)]).difference(set(channels[str(guild.id)])))
                member_doc.channels[str(guild.id)] = diff
                member_doc.update(set__channels=member_doc.channels)
                return True
            else:
                return None
        else:
            return None

    def get_subbed_channels(self, member, guild):
        member_doc = self.get_member_document(member.id)
        return member_doc.channels[str(guild.id)] if member_doc is not None and str(guild.id) in member_doc.channels else None

    def get_user_whitelist(self, ctx):
        member = ctx.author
        member_doc = self.get_member_document(member.id)
        if member_doc is not None:
            # return member_doc.whitelist
            whitelist_doc = self.get_whitelist_document({
                'guild_id' : str(ctx.guild.id),
                'user_id' : str(ctx.author.id)
            })
            return whitelist_doc.whitelist if whitelist_doc is not None else None
        else:
            return None

    def whitelist_add(self, ctx, channel_id, whitelist):
        # Check if Member exists in DB.
        member_doc = self.get_member_document(ctx.author.id)
        key = {
            'guild_id' : str(ctx.guild.id),
            'user_id' : str(ctx.author.id)
        }
        if member_doc is not None:
            # Find whitelist document for user.
            whitelist_doc = self.get_whitelist_document(key)
            if whitelist_doc is not None:
                # Update whitelist document.
                # Update whitelist. Check if user has whitelist for channel.
                if str(channel_id) in whitelist_doc.whitelist:
                    current_wl = whitelist_doc.whitelist[str(channel_id)]
                    whitelist_doc.whitelist[str(channel_id)] = list(set(current_wl).union(set(whitelist[str(channel_id)])))
                    whitelist_doc.update(set__whitelist=whitelist_doc.whitelist)
                else:
                    whitelist_doc.whitelist.update(whitelist)
                    whitelist_doc.update(set__whitelist=whitelist_doc.whitelist)
            else:
                GuildMemberWhitelist(key, whitelist, True).save()
        else:
            # If member doesn't exist, create and save.
            GuildMember(str(ctx.author.id), ctx.author.name, {
                'channels' : [str(channel_id)]
            }).save()
            GuildMemberWhitelist(key, whitelist, True).save()

    def get_member_document(self, id):
        query = GuildMember.objects(user_id=str(id))
        if len(query) == 0:
            return None
        else:
            return query[0]
    def get_whitelist_document(self, key):
        query = GuildMemberWhitelist.objects(whitelist_id=key)
        if len(query) == 0:
            return None
        else:
            return query[0]

    def get_vc_document(self, id):
        query = VoiceChannel.objects(id=id)
        return query[0] if len(query) != 0 else None
            