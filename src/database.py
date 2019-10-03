from mongoengine import connect

class SubscribeDatabase:
    def __init__(self, name='subscriberbot'):
        self.connect_db(name)

    def connect_db(self, name):
        connect(name)