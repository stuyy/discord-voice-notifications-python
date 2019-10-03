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