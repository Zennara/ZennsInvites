import keep_alive
import discord
import os
import asyncio
import json
from datetime import datetime

#declare client
client = discord.Client()

#server-specific ids
guild_id = "696583117502152774"

#check invites and compare
invites = {}
last = ""
async def getInvites():
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
      #get user (member object)
      if (message.content == '!invites'):
        user = message.author
      else:
        user = message.guild.get_member(message.mentions[0].id)

      #get invites
      with open("database.json", 'r') as f:
        users = json.load(f)
        f.close()
      #check if user is in database
      if str(user.id) not in users:
        users[str(user.id)] = {'invites': 0, 'leaves': 0, 'joinCode': "null", 'inviter': "null"}
      Invites = users[str(user.id)]['invites']
      Leaves = users[str(user.id)]['leaves']
      totalInvites = Invites - Leaves

      #write new data to files
      with open("database.json", 'w') as f:
        json.dump(users, f)
        f.close()

      embed = discord.Embed(color=0x8a0303)
      embed.add_field(name=user.name + "#" + user.discriminator, value="You have **" + str(Invites) + "** invites! (**" + str(totalInvites) + "** regular, **-" + str(Leaves) + "** leaves)", inline=False)

      await message.channel.send(embed=embed)

    if message.content.startswith('!info'):
        #get user (member object)
        if (message.content == '!info'):
          user = message.author
        else:
          user = message.guild.get_member(message.mentions[0].id)

        #set embed
        embed = discord.Embed(color=0x8a0303)
        embed.set_author(name=user.name + "#" + user.discriminator)
        embed.add_field(name="ID:", value=user.id, inline=False)
        embed.set_thumbnail(url=user.avatar_url)

        #split created_at into date and time
        createDT = str(user.created_at).split()
        createdDate = createDT[0]
        createdTime = str(datetime.strptime(str(createDT[1][0 : len(createDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))

        #split joined_at into date and time
        joinedDT = str(user.joined_at).split()
        joinedDate = joinedDT[0]
        joinedTime = str(datetime.strptime(str(joinedDT[1][0 : len(joinedDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))

        embed.add_field(name="Joined Server at", value=joinedDate + " at " + joinedTime, inline=True)

        #join code
        with open("database.json", 'r') as f:
          users = json.load(f)
          try:
            jCode = users[str(user.id)]['joinCode']
          except:
            jCode = "null"
          embed.add_field(name="Join Code", value=jCode)
          f.close()

        #joined discord
        embed.add_field(name="Joined Discord at", value=createdDate + " at " + createdTime, inline=False)

        #if boosting display since when
        if (str(user.premium_since) != "None"):
          #split premium_since into date and time
          premiumDT = str(user.premium_since).split()
          premiumDate = premiumDT[0]
          premiumTime = str(datetime.strptime(str(premiumDT[1][0 : len(premiumDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))
          embed.add_field(name="Boosting Server since", value=premiumDate + " at " + premiumTime, inline=False)

        #requested by
        embed.set_footer(text="Requested by " + message.author.name + "#" + message.author.discriminator + "\nID: " + str(message.author.id))
        await message.channel.send(embed=embed)
      

@client.event
async def on_member_join(member):
  global last
  global lastName
  last = str(member.id)
  lastName = str(member.name)

  #wait until getInvites() is done
  await asyncio.sleep(5)

  #declare user
  with open("database.json", 'r') as f:
    users = json.load(f)
    f.close()

  #append join code
  if str(member.id) not in users:
    users[str(member.id)] = {'invites': 0, 'leaves': 0, 'joinCode': joinCode, 'inviter': codeOwner}
  users[str(member.id)]['joinCode'] = joinCode
  users[str(member.id)]['inviter'] = codeOwner

  #add to invites
  if codeOwner not in users:
    users[codeOwner] = {'invites': 0, 'leaves': 0, 'joinCode': "null", 'inviter': "null"}
  users[codeOwner]['invites'] += 1

  #write new data to files
  with open("database.json", 'w') as f:
    json.dump(users, f)
    f.close()

@client.event
async def on_member_remove(member):
  #wait for getInvites()
  await asyncio.sleep(5)

  #declare user
  with open("database.json", 'r') as f:
    users = json.load(f)
    f.close()

  #add to leaves
  if str(member.id) in users:
    if users[str(member.id)]['inviter'] != "null":
      users[users[str(member.id)]['inviter']]['leaves'] += 1

  #write new data to files
  with open("database.json", 'w') as f:
    json.dump(users, f)
    f.close()
  


client.loop.create_task(getInvites())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by users
client.run(os.environ.get("TOKEN"))