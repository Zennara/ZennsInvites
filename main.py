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
client.run(os.environ.get("DISCORD_BOT_SECRET"))