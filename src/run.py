from SubscribeBot import SubscriberBot
import os

client = SubscriberBot(command_prefix='-')
client.run(os.getenv("TOKEN"))