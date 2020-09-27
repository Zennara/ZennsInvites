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
guild = client.get_guild(int(guild_id))

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
  global bumped
  bumped = False
  print("\nZennInvites Ready\n")
  with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()
  await client.change_presence(activity=discord.Streaming(name=data["prefix"] + "help", url="https://www.twitch.tv/xzennara/about"))
    
@client.event
async def on_message(message):
    global bumped
    #get prefix
    with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()
    prefix = data["prefix"]

    #print((await message.channel.fetch_message(759836810469048373)).embeds[0].colour)

    #split current datetime
    nowDT = str(datetime.now()).split()
    nowDate = nowDT[0]
    nowTime = str(datetime.strptime(str(nowDT[1][0 : len(nowDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))

    #help
    if message.content == prefix + 'help':
      embed = discord.Embed(color=0x8a0303)
      embed.set_author(name=client.user.name + " Help", icon_url=client.user.avatar_url)
      start = "`" + prefix + "help"
      embed.add_field(name="Counters", value=start + " counters`", inline=False)
      embed.add_field(name="Invites", value=start + " invites`", inline=False)
      embed.add_field(name="Role Reactions", value=start + " reactions`", inline=False)
      embed.add_field(name="Commands", value=start + " commands`", inline=False)
      embed.add_field(name="Disboard", value=start + " disboard`", inline=False)
      embed.set_footer(text="______________________\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #add counter
    if message.content.startswith(prefix + "addcounter"):
      guild = client.get_guild(int(guild_id))

      foundCategory = False
      #find category
      for category in guild.categories:
        if category.name == "Server Stats":
          categoryObject = category
          foundCategory = True
          break
      #create category
      if foundCategory == False:
        categoryObject = await guild.create_category("Server Stats", overwrites=None, reason=None)

      #get amount of bots
      bots = 0
      for member in guild.members:
        if member.bot:
          bots += 1
      
      cont = False
      #get channel creation type
      if message.content == prefix + "addcounter members":
        channelName = "Members"
        channelType = guild.member_count - bots
        cont = True

      if message.content == prefix + "addcounter bots":
        channelName = "Bots"
        channelType = bots
        cont = True
        
      foundChannel = False
      if cont:
        #find channel
        for channel in guild.channels:
          if channel.name.startswith(channelName + ":"):
            channelObject = channel
            foundChannel = True
            break
        #create channel
        if foundChannel == False:
          channelObject = await guild.create_voice_channel(f"{channelName}: {channelType}",   overwrites=None, category=categoryObject, reason=None)
          await channelObject.set_permissions(guild.default_role, connect = False)
      

    #check bump disboard
    if message.content == '!d bump':
      bumped = True
      #get user (member object)
      global user
      user = message.author
    #check disboard bot reply
    elif bumped == True:
      if str(message.embeds[0].colour) == "#24b7b7":
        if str(user.id) not in data:
          data[str(user.id)] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
        data[str(user.id)]['bumps'] += 1
      bumped = False

    #disboard bumps
    if message.content.startswith(prefix + 'd bumps'):
      #get user (member object)
      if (message.content == prefix + 'd bumps'):
        user = message.author
      else:
        user = message.guild.get_member(message.mentions[0].id)

      #check if user is in database
      if str(user.id) not in data:
        data[str(user.id)] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
      bumps = data[str(user.id)]['bumps']

      #send embed
      embed = discord.Embed(color=0x8a0303)
      embed.add_field(name=user.name + "#" + user.discriminator, value="You have bumped the server **" + str(bumps) + "** times!", inline=False)
      embed.set_footer(text=nowDate + " at " + nowTime)
      await message.channel.send(embed=embed)

    #edit bumps
    if message.content.startswith(prefix + "d editbumps"):
      #get user (member object)
      user = message.guild.get_member(message.mentions[0].id)
      
      #get previous bumps amount
      prevBumps = data[str(user.id)]['bumps']

      try:
        editBumpAmount = int(message.content.split()[3])
        data[str(user.id)]['bumps'] = editBumpAmount

        #send embed
        embed = discord.Embed(color=0x8a0303)
        embed.add_field(name=user.name + "#" + user.discriminator, value="User now has **" + str(data[str(user.id)]['bumps']) + "** bumps! (Original: **" + str(prevBumps) + "**)", inline=False)
        embed.set_footer(text=nowDate + " at " + nowTime)
        await message.channel.send(embed=embed)
      except:
        print('')

    #help invites (InviteManager)
    if message.content == prefix + 'help invites':
      embed = discord.Embed(color=0x8a0303)
      embed.set_author(name=client.user.name + " Invites Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "invites [member]`", value="Shows how many invites the user has", inline=False)
      embed.add_field(name="`"+prefix+ "leaderboard`", value="Shows the invites leaderboard", inline=False)
      embed.add_field(name="`"+prefix+ "editinvites <member> <amount>`", value="Set invites of a user", inline=False)
      embed.add_field(name="`"+prefix+ "editleaves <member> <amount>`", value="Set leaves of a user", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help reactions (Zira)
    if message.content == prefix + 'help reactions':
      embed = discord.Embed(color=0x8a0303)
      embed.set_author(name=client.user.name + " Reactions Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "rr <channelID> <messageID> <reaction> <role>`", value="Give a role when user reacts to message", inline=False)
      embed.add_field(name="`"+prefix+ "delrr <channelID> <messageID>`", value="Remove a reaction role", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help stats (Server Stats)
    if message.content == prefix + 'help counters':
      embed = discord.Embed(color=0x8a0303)
      embed.set_author(name=client.user.name + " Counters Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "addcounter <tracker>`", value="Make a new server counter", inline=False)
      embed.add_field(name="`"+prefix+ "delcounter <tracker>`", value="Delete a server counter", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help commands
    if message.content == prefix + 'help commands':
      embed = discord.Embed(color=0x8a0303)
      embed.add_field(name="`"+prefix+ "info [member]`", value="Show info about a member", inline=False)
      embed.add_field(name="`"+prefix+ "prefix <prefix>`", value="Change the command prefix", inline=False)
      embed.set_author(name=client.user.name + " Commands Help", icon_url=client.user.avatar_url)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help disboard
    if message.content == prefix + 'help disboard':
      embed = discord.Embed(color=0x8a0303)
      embed.add_field(name="`"+prefix+ "d leaderboard`", value="Show the disboard bump leaderboard", inline=False)
      embed.add_field(name="`"+prefix+ "d bumps [member]`", value="Show how many bumps a user has", inline=False)
      embed.add_field(name="`"+prefix+ "d editbumps <member> <amount>`", value="Set bumps of a member", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)
    
    #change prefix
    if message.content.startswith(prefix + 'prefix '):
      data["prefix"] = message.content.split()[1]
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
        data[str(user.id)] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
      Invites = data[str(user.id)]['invites']
      Leaves = data[str(user.id)]['leaves']
      totalInvites = Invites - Leaves

      embed = discord.Embed(color=0x8a0303)
      embed.add_field(name=user.name + "#" + user.discriminator, value="You have **" + str(Invites) + "** invites! (**" + str(totalInvites) + "** regular, **-" + str(Leaves) + "** leaves)", inline=False)

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
            data[str(user.id)] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
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

    #write new data to files
    with open("database.json", 'w') as f:
      json.dump(data, f)
      f.close()

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
    data[str(member.id)] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': joinCode, 'inviter': codeOwner}
  data[str(member.id)]['joinCode'] = joinCode
  data[str(member.id)]['inviter'] = codeOwner

  #add to invites
  if codeOwner not in data:
    data[codeOwner] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
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