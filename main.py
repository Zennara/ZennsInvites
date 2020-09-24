import keep_alive
import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print("-----------------")
    print(client.user)
    print("-----------------")

#end
keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by users
client.run(os.environ.get("TOKEN"))