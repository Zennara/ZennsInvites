import keep_alive
import discord
import os
import asyncio
import json

client = discord.Client()

f = open('database.json')
users = json.load(f)
f.close()

#Writing JSON data
with open("database.json", 'w') as f:
  json.dump(users, f)
  f.close()

@client.event
async def on_ready():
    print("\nZennInvites Ready")
    
@client.event
async def on_message(message):
    if message.content.startswith('!invites'):
        totalInvites = 0
        for i in await message.guild.invites():
            if i.inviter == message.author:
                totalInvites += i.uses
        await message.channel.send("You've invited " + str(totalInvites) + " members(s) to the server!")

    #if message.content.startswith('!db'):
      

@client.event
async def on_member_join(member):
  if member.id not in users:
    users[member.id] = {'invites': 0, 'leaves': 0}
  users[member.id]['invites'] = users[member.id]['invites'] + 1
  with open("database.json", 'w') as f:
    json.dump(users, f)
    f.close()


#client.loop.create_task(PushInvites())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by users
client.run(os.environ.get("TOKEN"))