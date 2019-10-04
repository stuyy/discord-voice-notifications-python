from mongoengine import connect
from models.MemberCollections import GuildMember

class Database:
    def __init__(self, name='subscriberbot'):
        self.connect_db(name)

    def connect_db(self, name):
        connect(name)
    def subscribe(self, channels, ctx):
        member = ctx.author
        query = GuildMember.objects(user_id=str(member.id))
        if len(query) == 0:
            member_doc = GuildMember(str(member.id), str(member.name), {}, channels)
            member_doc.save()
        else:
            member_doc = query[0]
            member_doc.channels.update(channels)
            member_doc.update(set__channels=member_doc.channels)

    def unsubscribe(self, channels, ctx):
        member = ctx.author
        # Get the member document first.
        query = GuildMember.objects(user_id=str(member.id))
        if len(query) == 0:
            pass
        else:
            member_doc = query[0]
            subscribed = member_doc.channels
            print(subscribed)
            channel_ids = channels.keys()
            for ids in channel_ids:
                if ids in channel_ids:
                    print('yes')
                    member_doc.channels.pop(ids, None)
            
            member_doc.update(set__channels=member_doc.channels)

    def get_subbed_channels(self, ctx):
        member = ctx.author
        member_id = member.id
        member_doc = self.get_member_document(member_id)
        return member_doc.channels if member_doc is not None else None

    def get_user_whitelist(self, ctx):
        member = ctx.author
        member_doc = self.get_member_document(member.id)
        if member_doc is not None:
            return member_doc.whitelist
        else:
            return None

    def get_member_document(self, id):
        query = GuildMember.objects(user_id=str(id))
        if len(query) == 0:
            return None
        else:
            return query[0]

    def whitelist_add(self, ctx):
        pass