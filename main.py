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
  with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()
  await client.change_presence(activity=discord.Game(name=data["prefix"] + "help"))
    
@client.event
async def on_message(message):
    #get prefix
    with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()
    prefix = data["prefix"]

    #help
    if message.content == prefix + 'help':
      embed = discord.Embed(color=0x8a0303)
      embed.set_author(name=client.user.name + " Help", icon_url=client.user.avatar_url)
      start = "`" + prefix + "help"
      embed.add_field(name="Counters", value=start + "stats`", inline=False)
      embed.add_field(name="Invites", value=start + " invites`", inline=False)
      embed.add_field(name="Role Reactions", value=start + " reactions`", inline=False)
      embed.add_field(name="Commands", value=start + " commands`", inline=False)
      await message.channel.send(embed=embed)

    #help invites (InviteManager)
    if message.content == prefix + 'help invites':
      embed = discord.Embed(color=0x8a0303)
      embed.set_author(name=client.user.name + " Invites Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "invites [member]`", value="Shows how many invites the user has", inline=False)
      embed.add_field(name="`"+prefix+ "leaderboard`", value="Shows the invites leaderboard", inline=False)
      embed.add_field(name="`"+prefix+ "editinvites <member>`", value="Add or subtract invites from a user", inline=False)
      embed.add_field(name="`"+prefix+ "editleaves <member>`", value="Add or subtract invites from a user", inline=False)
      await message.channel.send(embed=embed)

    #help reactions (Zira)
    if message.content == prefix + 'help reactions':
      embed = discord.Embed(color=0x8a0303)
      embed.set_author(name=client.user.name + " Reactions Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "rr <channelID> <messageID> <reaction> <role>`", value="Give a role when user reacts to message", inline=False)
      embed.add_field(name="`"+prefix+ "delrr <channelID> <messageID>`", value="Remove a reaction role", inline=False)
      await message.channel.send(embed=embed)

    #help stats (Server Stats)
    if message.content == prefix + 'help counters':
      embed = discord.Embed(color=0x8a0303)
      embed.set_author(name=client.user.name + " Counters Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "addcounter <tracker>`", value="Make a new server counter", inline=False)
      embed.add_field(name="`"+prefix+ "delcounter <tracker>`", value="Delete a server counter", inline=False)
      await message.channel.send(embed=embed)

    #help commands
    if message.content == prefix + 'help commands':
      embed = discord.Embed(color=0x8a0303)
      embed.add_field(name="`"+prefix+ "info [member]`", value="Show info about a member", inline=False)
      embed.add_field(name="`"+prefix+ "prefix <prefix>`", value="Change the command prefix", inline=False)
      embed.set_author(name=client.user.name + " Commands Help", icon_url=client.user.avatar_url)
      await message.channel.send(embed=embed)
    
    #change prefix
    if message.content.startswith(prefix + 'prefix '):
      data["prefix"] = message.content.split()[1]
      with open("database.json", 'w') as f:
        json.dump(data, f)
        f.close()
      await client.change_presence(activity=discord.Game(name=data["prefix"] + "help"))

    #only run on guild_id server
    if message.content.startswith(prefix + 'invites') and str(message.guild.id) == guild_id:
      #get user (member object)
      if (message.content == prefix + 'invites'):
        user = message.author
      else:
        user = message.guild.get_member(message.mentions[0].id)

      #check if user is in database
      if str(user.id) not in data:
        data[str(user.id)] = {'invites': 0, 'leaves': 0, 'joinCode': "null", 'inviter': "null"}
      Invites = data[str(user.id)]['invites']
      Leaves = data[str(user.id)]['leaves']
      totalInvites = Invites - Leaves

      #write new data to files
      with open("database.json", 'w') as f:
        json.dump(data, f)
        f.close()

      embed = discord.Embed(color=0x8a0303)
      embed.add_field(name=user.name + "#" + user.discriminator, value="You have **" + str(Invites) + "** invites! (**" + str(totalInvites) + "** regular, **-" + str(Leaves) + "** leaves)", inline=False)

      #split current datetime
      nowDT = str(datetime.now()).split()
      nowDate = nowDT[0]
      nowTime = str(datetime.strptime(str(nowDT[1][0 : len(nowDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))

      embed.set_footer(text=nowDate + " at " + nowTime)

      await message.channel.send(embed=embed)

    if message.content.startswith(prefix + 'info'):
        #get user (member object)
        if (message.content == prefix + 'info'):
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

        embed.add_field(name="Joined Server at", value=joinedDate + " at " + joinedTime, inline=False)

        #join code and owner, only run on guild_id server
        if str(message.guild.id) == guild_id:
          if str(user.id) not in data:
            data[str(user.id)] = {'invites': 0, 'leaves': 0, 'joinCode': "null", 'inviter': "null"}
          with open("database.json", 'w') as f:
            json.dump(data, f)
            f.close()
          jCode = data[str(user.id)]['joinCode']

          embed.add_field(name="Join Code", value=jCode, inline=True)
          if data[str(user.id)]['inviter'] != "null":
            inviterMember = message.guild.get_member(int(data[str(user.id)]['inviter']))
            embed.add_field(name="Owned By", value=inviterMember.name + "#" + inviterMember.discriminator, inline=True)

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
    data = json.load(f)
    f.close()

  #append join code
  if str(member.id) not in data:
    data[str(member.id)] = {'invites': 0, 'leaves': 0, 'joinCode': joinCode, 'inviter': codeOwner}
  data[str(member.id)]['joinCode'] = joinCode
  data[str(member.id)]['inviter'] = codeOwner

  #add to invites
  if codeOwner not in data:
    data[codeOwner] = {'invites': 0, 'leaves': 0, 'joinCode': "null", 'inviter': "null"}
  data[codeOwner]['invites'] += 1

  #write new data to files
  with open("database.json", 'w') as f:
    json.dump(data, f)
    f.close()

@client.event
async def on_member_remove(member):
  #wait for getInvites()
  await asyncio.sleep(5)

  #declare user
  with open("database.json", 'r') as f:
    data = json.load(f)
    f.close()

  #add to leaves
  if str(member.id) in data:
    if data[str(member.id)]['inviter'] != "null":
      data[data[str(member.id)]['inviter']]['leaves'] += 1

  #write new data to files
  with open("database.json", 'w') as f:
    json.dump(data, f)
    f.close()
  


client.loop.create_task(getInvites())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by data
client.run(os.environ.get("TOKEN"))