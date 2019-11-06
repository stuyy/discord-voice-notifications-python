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

    def get_user_whitelist(self, ctx):
        user_id = str(ctx.author.id)
        wl_doc = VoiceChannelWhitelist.objects(id__guild_id=str(ctx.guild.id), id__user_id=user_id)
        return wl_doc

    def get_whitelisters(self, ctx):
        user_id = str(ctx.author.id)
        wl_doc = VoiceChannelWhitelist.objects(id__guild_id=str(ctx.guild.id), id__user_id=user_id)
        for x in wl_doc:
            print(x.whitelisters)

    '''
    Get the VoiceChannel document and VoiceChannelWhitelist Document.
    If both of them exist, continue. If they both are None, then it could mean two things:
        - The VoiceChannel document returns None if it is not in the DB, which means no one has subscribed to the 
        Channel yet.
        - The VoiceChannel document is not None, but the Whitelist document is None. This means the user has not subscribed
        to any channels yet. It's important to remember when a user subscribes to a channel, they automatically get a Whitelist
        Document created for them. 
    
    Base Case: Check if user is actually subscribed to the channel, if they are not, return false.

    Loop through all user IDs the author is whitelisting. For each user to be whitelisted, check if they have a Whitelist Document in the Database.

    If whitelist document exists, then we need to add the author's ID to the 'user to be whitelisted's "whitelisters" list property.

    If whitelist document does not exist, this means the user has not subscribed to that channel, so create a document for them
    and set their whitelisters list propert to the author's ID.

    We then need to update the author's whitelist, adding the ID of the user to be whitelisted to the author's whitelist list property.
    '''
    def whitelist_add(self, ctx, channel_id, whitelist):

        is_subbed = self.is_subscribed(str(ctx.author.id), str(channel_id), str(ctx.guild.id))
        if is_subbed == False:
            return False
        
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
            return False
    '''
        Remove the users from the author's whitelist property
        Remove the author from the user's whitelisters property.
    '''
    def whitelist_remove(self, ctx, channel_id, users):
        is_subbed = self.is_subscribed(str(ctx.author.id), str(channel_id), str(ctx.guild.id))
        if is_subbed == False:
            return False

        vc_doc = self.get_vc_document(str(channel_id), str(ctx.guild.id))
        wl_doc = self.get_vc_whitelist_document(channel_id, ctx.guild.id, ctx.author.id)

        if vc_doc is not None and wl_doc is not None:
            whitelisted_users = wl_doc.whitelist
            for u in users[str(channel_id)]:
                print(u)
                if u in whitelisted_users:  # If user id in whitelist list from DB, remove. 
                    whitelisted_users.remove(u)
            # Update the document.
            wl_doc.update(set__whitelist=whitelisted_users)
            print('done')
            
            # We removed the users from author's whitelist, now we need to iterate through all the users we removed, and remove author from their whitelister list.
            for u in users[str(channel_id)]:
                print('Removing ' + u)
                other = self.get_vc_whitelist_document(channel_id, ctx.guild.id, str(u))
                if other is not None:
                    print(other.whitelisters)
                    if str(ctx.author.id) in other.whitelisters:
                        other.whitelisters.remove(str(ctx.author.id))
                        other.update(set__whitelisters=wl_doc.whitelisters)
                        print('done')
            print("finished.")
        else:
            print('wtf?')

    def is_subscribed(self, user_id, voice_id, guild_id):
        vc_doc = self.get_vc_document(voice_id, guild_id)
        if vc_doc is not None:
            if user_id in vc_doc.subscribed_users:
                return True
            else:
                return False
        else: # VoiceChannel document doesn't exist. Means no one has subscribed to it.
            return False
    def get_all_subbed_users(self, voice_id, guild_id, user_id):
        vc_document = self.get_vc_document(voice_id, guild_id)
        wl_document = self.get_vc_whitelist_document(voice_id, guild_id, user_id)
        if vc_document is not None and wl_document is not None:
            return wl_document.whitelisters
        else:
            pass
    '''
        Utility Functions
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
            
    