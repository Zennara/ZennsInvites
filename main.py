import keep_alive
import discord
import os
import asyncio
import json
from discord.utils import get

client = discord.Client()

guild_id = "696583117502152774"
invites = {}
last = ""

async def fetch():
 global last
 global invites
 global codeOwner
 global joinCode
 await client.wait_until_ready()
 gld = client.get_guild(int(guild_id))
 while True:
  invs = await gld.invites()
  tmp = []
  for i in invs:
   for s in invites:
    if s[0] == i.code:
     if int(i.uses) > s[1]:
      #get inviter id
      codeOwner = str(i.inviter.id)
      joinCode = str(i.code)
   tmp.append(tuple((i.code, i.uses)))
  invites = tmp
  await asyncio.sleep(4)

@client.event
async def on_ready():
  print("\nZennInvites Ready\n")
    
@client.event
async def on_message(message):
    if message.content.startswith('!invites'):
        totalInvites = 0
        for i in await message.guild.invites():
            if i.inviter == message.author:
                totalInvites += i.uses
        await message.channel.send("You've invited " + str(totalInvites) + " members(s) to the server!")

    if message.content.startswith('!info '):
        user = message.guild.get_member(message.mentions[0].id)
        embedVar = discord.Embed(title=user.name, color=0x8a0303)
        embedVar.add_field(name="ID:", value=message.mentions[0].id, inline=False)
        embedVar.add_field(name="Date Created:", value=user.created_at, inline=False)
        await message.channel.send(embed=embedVar)
      

@client.event
async def on_member_join(member):
  global last
  global lastName
  last = str(member.id)
  lastName = str(member.name)

  #wait until fetch() is done
  await asyncio.sleep(5)

  #declare users{}
  with open("database.json", 'r') as f:
    users = json.load(f)
    f.close()

  #append join code
  if str(member.id) not in users:
    users[str(member.id)] = {'invites': 0, 'leaves': 0, 'joinCode': joinCode}
  users[str(member.id)]['joinCode'] = joinCode

  #add to invites
  if codeOwner not in users:
    users[codeOwner] = {'invites': 0, 'leaves': 0, 'joinCode': "null"}
  users[codeOwner]['invites'] += 1

  #write new data to files
  with open("database.json", 'w') as f:
    json.dump(users, f)
    f.close()

client.loop.create_task(fetch())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by users
client.run(os.environ.get("TOKEN"))