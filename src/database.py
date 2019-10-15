from mongoengine import connect
from models.MemberCollections import *

class Database:
    def __init__(self, name='subscriberbot'):
        self.connect_db(name)

    def connect_db(self, name):
        connect(name)
        
    def subscribe(self, channels, ctx):
        for id in channels[str(ctx.guild.id)]:
            vc_doc = self.get_vc_document(id, str(ctx.guild.id))
            user_id = str(ctx.author.id)
            user = {
                user_id : {
                    "whitelist": [],
                    "whitelist_enabled": False
                }
            }
            if vc_doc is None:
                VoiceChannel(id={ "vc_id": id, "guild_id" : str(ctx.guild.id)}, subscribed_users=user).save()
            else:
                subbed = vc_doc.subscribed_users
                if str(ctx.author.id) not in subbed:
                    subbed[(str(ctx.author.id))] = {
                        "whitelist" : [],
                        "whitelist_enabled" : False
                    }
                    vc_doc.update(set__subscribed_users=subbed)
                else:
                    print("Already exists.")

            wl_doc = self.get_vc_whitelist_document(id, ctx.guild.id, ctx.author.id)
            if wl_doc is None:
                VoiceChannelWhitelist(id={"vc_id" : str(id), "guild_id" : str(ctx.guild.id), "user_id" : str(ctx.author.id)}).save()
                print("Saved.")
            else:
                print("Do nothing. We're not updating their whitelist.")
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
        for id in channels[str(ctx.guild.id)]:
            vc_doc = self.get_vc_document(id, str(ctx.guild.id))
            if vc_doc is None:
                print("Voice Channel Document does not exist.")
            else:
                # Check if User is Subscribed.
                subbed = vc_doc.subscribed_users
                popped = subbed.pop(str(ctx.author.id), None)
                if popped is not None:
                    vc_doc.update(set__subscribed_users=subbed)
            
        '''member = ctx.author
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
            return None'''

    '''
        This function must return a list of all the voice channel ids the user is subscribed to.
    '''
    def get_subbed_channels(self, member, guild):
        query = VoiceChannel.objects(id__guild_id=str(guild.id))
        subbed_channels = []
        for q in query:
            print(q.id['vc_id'])
            if str(member.id) in q.subscribed_users:
                subbed_channels.append(q.id['vc_id'])

        return subbed_channels
        '''
        member_doc = self.get_member_document(member.id)
        return member_doc.channels[str(guild.id)] if member_doc is not None and str(guild.id) in member_doc.channels else None
        '''
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
        vc_doc = self.get_vc_document(str(channel_id), str(ctx.guild.id))
        # Get the author's whitelist.
        wl_doc = self.get_vc_whitelist_document(channel_id, ctx.guild.id, ctx.author.id)
        if vc_doc is not None and wl_doc is not None:
            for user_id in whitelist[str(channel_id)]:
                # Get the user to whitelist's whitelist doc. If None, create one for them.
                user_wl_doc = self.get_vc_whitelist_document(channel_id, ctx.guild.id, user_id)
                if user_wl_doc is not None:
                    whitelisters = user_wl_doc.whitelisters
                    if user_id not in whitelisters:
                        whitelisters.append(str(ctx.author.id))
                        user_wl_doc.update(set__whitelisters=whitelisters)
                    else:
                        print("is in")
                else:
                    # If none, create and add.
                    VoiceChannelWhitelist(id={ "vc_id" : str(channel_id), "guild_id" : str(ctx.guild.id), "user_id" : user_id}, whitelisters=[str(ctx.author.id)], enabled=False, whitelist=[]).save()

                # Now update the author's whitelist.
                if user_id in wl_doc.whitelist:
                    print("skip")
                else:
                    wl_doc.whitelist.append(user_id)
                    wl_doc.enabled=True
                    wl_doc.update(set__enabled=wl_doc.enabled)
                    wl_doc.update(set__whitelist=wl_doc.whitelist)
                print("done.")
            
        else:
            print("no doesnt exist")
        '''
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
        '''
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

    def get_vc_document(self, id, guild_id):
        query = VoiceChannel.objects(id={ "vc_id" : id, "guild_id" : guild_id})
        return query[0] if len(query) != 0 else None

    def get_vc_whitelist_document(self, voice_id, guild_id, user_id):
        query = VoiceChannelWhitelist.objects(id={
            "vc_id" : str(voice_id),
            "guild_id" : str(guild_id),
            "user_id" : str(user_id)
        })
        return query[0] if len(query) != 0 else None
            
    def get_all_subbed_users(self, voice_id, guild_id, user_id):
        vc_document = self.get_vc_document(voice_id, guild_id)
        wl_document = self.get_vc_whitelist_document(voice_id, guild_id, user_id)
        if vc_document is not None and wl_document is not None:
            return wl_document.whitelisters
        else:
            pass