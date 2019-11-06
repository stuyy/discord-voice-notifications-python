from dotenv import load_dotenv
from discord.ext import commands
from SubscribeBot import SubscribeBot
from database import Database
import os

db = Database()

client = SubscribeBot(db, command_prefix='?', case_insensitive=True)
exts = ['cogs.Subscribe', 'cogs.Whitelist', 'cogs.RoleReactions', 'cogs.VoiceEvents']

if __name__ == '__main__':
    for f in os.listdir("./src/cogs"):
        p = f.find(".py")
        if p != -1:
            ext = "cogs." + f[0:p]
            client.load_extension(ext)
            print("Loaded " + ext)
    
    if os.getenv("MODE") == "DEV":
        print("DEV MODE")
    elif os.getenv("MODE") == "PROD":
        load_dotenv()
    client.run(os.getenv("TOKEN"))