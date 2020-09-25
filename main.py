import keep_alive
import discord
import os
import asyncio
import json

client = discord.Client()

#f = open('invites.json')
#invites = json.load(f)
#f.close()


guild_id = "696583117502152774"
logs_channel = "696589280344145991"
invites = {}
last = ""

async def fetch():
 global last
 global invites
 global codeOwner
 await client.wait_until_ready()
 gld = client.get_guild(int(guild_id))
 logs = client.get_channel(int(logs_channel))
 while True:
  invs = await gld.invites()
  tmp = []
  for i in invs:
   for s in invites:
    if s[0] == i.code:
     if int(i.uses) > s[1]:
      usr = gld.get_member(int(last))
      testh = f"{usr.name} **joined**; Invited by **{i.inviter.name}** (**{str(i.uses)}** invites)"
      await logs.send(testh)

      #get inviter id
      codeOwner = str(i.inviter.id)
   tmp.append(tuple((i.code, i.uses)))
  invites = tmp
  await asyncio.sleep(4)

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
  global last
  last = str(member.id)

  #wait until fetch() is done
  await asyncio.sleep(5)

  #count invites
  with open("database.json", 'r') as f:
    users = json.load(f)
    f.close()
  with open("database.json", 'w') as f:
    if codeOwner not in users:
      users[codeOwner] = {'invites': 0, 'leaves': 0}
    users[codeOwner]['invites'] += 1
    f.close()

  #write new data to files
  with open("database.json", 'w') as f:
    json.dump(users, f)
    f.close()

#client.loop.create_task(PushInvites())
client.loop.create_task(fetch())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by users
client.run(os.environ.get("TOKEN"))