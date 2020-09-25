import keep_alive
import discord
import os
import asyncio
from replit import db
import json

client = discord.Client()


data = {}
data['users'] = []
data['users'].append({
    'name': 'Zennara#8377',
    'invites': 50,
    'left': 15
})

#Writing JSON data
with open("database.json", 'w') as f:
  json.dump(data, f)

@client.event
async def on_ready():
    print("ZennInvites Ready")

x = input()
if x == "test":
  with open('database.json', 'r') as file:
     json_data = json.load(file)
     for item in json_data:
           if item['name'] in ['Zennara#8377']:
              item['name'] = "test"
  with open('/path/to/josn_file.json', 'w') as file:
      json.dump(json_data, file, indent=2)
    
@client.event
async def on_message(message):
    if message.content.startswith('!invites'):
        totalInvites = 0
        for i in await message.guild.invites():
            if i.inviter == message.author:
                totalInvites += i.uses
        await message.channel.send("You've invited " + str(totalInvites) + " members(s) to the server!")
    if message.content.startswith('!db'):
      invites = db[str(message.author)]
      print("You've invited" + invites + " member(s) to the server!")

@client.event
async def on_member_join(member):
  with open('database.json') as json_file:
    data = json.load(json_file)
    for p in data['users']:
        print('name: ' + p['name'])
        print('Website: ' + p['website'])
        print('From: ' + p['from'])
        print('')

  



#client.loop.create_task(PushInvites())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by users
client.run(os.environ.get("TOKEN"))