#CastleMiner Discord bot, made by Zennara#8377
#This is a custom discord bot. It is written to work on only one server.

#imports
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
  await asyncio.sleep(1)

async def checkCounters():
  while True:
    #discord API limits rates to twice every 10m for channel edits
    await asyncio.sleep(600)

    guild = client.get_guild(int(guild_id))
    #get amount of bots
    bots = 0
    for member in guild.members:
      if member.bot:
        bots += 1

    #get data
    with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()

    #update channels
    for channel in guild.voice_channels:
      if channel.name.startswith("Members"):
        await channel.edit(name="Members: " + str(guild.member_count - bots))
      if channel.name.startswith("Bots"):
        await channel.edit(name="Bots: " + str(bots))
      if channel.name.startswith("Channels"):
        await channel.edit(name="Channels: " + str(len(guild.text_channels) + len(guild.voice_channels) - len(guild.categories)))
      if channel.name.startswith("Text Channels"):
        await channel.edit(name="Text Channels: " + str(len(guild.text_channels)))
      if channel.name.startswith("Voice Channels"):
        await channel.edit(name="Voice Channels: " + str(len(guild.voice_channels)))
      if channel.name.startswith("Categories"):
        await channel.edit(name="Categories: " + str(len(guild.categories)))
      if channel.name.startswith("Roles"):
        await channel.edit(name="Roles: " + str(len(guild.roles)))
      if channel.name.startswith("Bans"):
        await channel.edit(name="Bans: " + str(len(await guild.bans())))
      if channel.name.startswith("Messages"):
        await channel.edit(name="Messages: " + str(data['messages']))

@client.event
async def on_ready():
  global bumped
  bumped = False
  print("\nZennInvites Ready\n")
  with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()
  await client.change_presence(activity=discord.Streaming(name=" | " + data["prefix"] + "help", url="https://www.twitch.tv/xzennara/about"))  

@client.event
async def on_message(message):
    global user
    global bumped
    #get prefix
    with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()
    prefix = data["prefix"]

    #get messages and add
    data["messages"] += 1

    #set message content to lowercase
    messagecontent = message.content.lower()

    #split current datetime
    nowDT = str(datetime.now()).split()
    nowDate = nowDT[0]
    nowTime = str(datetime.strptime(str(nowDT[1][0 : len(nowDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))

    #update database
    if messagecontent == prefix + "database":
      if str(message.author.id) not in data:
        #loading message
        embed = discord.Embed(color=0x593695, description="**Loading Users Into Database...**")
        embed.set_author(name="@" + client.user.name + "#" + client.user.discriminator, icon_url=client.user.avatar_url)
        embed.set_footer(text=nowDate + " at " + nowTime)
        message2 = await message.channel.send(embed=embed)

        #invites
        for member in message.guild.members:
          totalInvites = 0
          for i in await message.guild.invites():
            if i.inviter == member:
              totalInvites += i.uses
          #add member to database
          if str(member.id) not in data:
            data[str(member.id)] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
          data[str(member.id)]['invites'] = totalInvites

        await message2.delete()
      else:
        embed = discord.Embed(color=0x593695, description="**Database has already been uploaded.**")
        embed.set_author(name="@" + client.user.name + "#" + client.user.discriminator, icon_url=client.user.avatar_url)
        embed.set_footer(text=nowDate + " at " + nowTime)
        await message.channel.send(embed=embed)

    #put users in database
    if str(message.author.id) not in data:
      data[str(message.author.id)] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}

    try:
      if str(message.guild.get_member(message.mentions[0].id)) not in data:
        data[str(message.guild.get_member(message.mentions[0].id).id)] = {'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
    except:
      pass

    #edit amounts
    if messagecontent.startswith(prefix + "edit"):
      #run in try's in case of error
      #get user (member object)
      try:
        user = message.guild.get_member(message.mentions[0].id)
      except:
        user = message.author
      try:      
        #get type
        editType = messagecontent.split()[1]

        #get previous invites amount
        prevAmount = data[str(user.id)][str(editType)]

        editAmount = int(messagecontent.split()[2])

        if editType == "invites" or editType == "leaves" or editType == "bumps":
          data[str(user.id)][str(editType)] = editAmount

          #send embed
          embed = discord.Embed(color=0x593695, description="User now has **" + str(editAmount) + "** " + editType + "!" + " (Original: **" + str(prevAmount) + "**)")
          embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar_url)
          embed.set_footer(text=nowDate + " at " + nowTime)
          await message.channel.send(embed=embed)
      except:
        pass

    #help
    if messagecontent == prefix + 'help':
      embed = discord.Embed(color=0x593695)
      embed.set_author(name=client.user.name + " Help", icon_url=client.user.avatar_url)
      start = "`" + prefix + "help"
      embed.add_field(name="Counters", value=start + " counters`", inline=False)
      embed.add_field(name="Invites", value=start + " invites`", inline=False)
      embed.add_field(name="Role Reactions", value=start + " reactions`", inline=False)
      embed.add_field(name="Disboard", value=start + " disboard`", inline=False)
      embed.add_field(name="Commands", value=start + " commands`", inline=False)
      embed.set_footer(text="______________________\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #add counter
    if messagecontent.startswith(prefix + "addcounter"):
      guild = client.get_guild(int(guild_id))

      foundCategory = False
      #find category
      for category in guild.categories:
        if category.name == str(message.guild.name) + " Stats":
          categoryObject = category
          foundCategory = True
          break
      #create category
      if foundCategory == False:
        categoryObject = await guild.create_category(str(message.guild.name) + " Stats", overwrites=None, reason=None)

      #get amount of bots
      bots = 0
      for member in guild.members:
        if member.bot:
          bots += 1
      
      #get channels/ categories
      total_text_channels = len(guild.text_channels)
      total_voice_channels = len(guild.voice_channels)
      total_channels = total_text_channels  + total_voice_channels - len(guild.categories)

      cont = False
      #get channel creation type
      if messagecontent == prefix + "addcounter members":
        channelName = "Members"
        channelType = guild.member_count - bots
        cont = True
      if messagecontent == prefix + "addcounter bots":
        channelName = "Bots"
        channelType = bots
        cont = True
      if messagecontent == prefix + "addcounter channels":
        channelName = "Channels"
        channelType = total_channels + 1
        cont = True
      if messagecontent == prefix + "addcounter textchannels":
        channelName = "Text Channels"
        channelType = total_text_channels
        cont = True
      if messagecontent == prefix + "addcounter voicechannels":
        channelName = "Voice Channels"
        channelType = total_voice_channels + 1
        cont = True
      if messagecontent == prefix + "addcounter categories":
        channelName = "Categories"
        channelType = len(guild.categories)
        cont = True
      if messagecontent == prefix + "addcounter bans":
        channelName = "Bans"
        channelType = len(await guild.bans())
        cont = True
      if messagecontent == prefix + "addcounter roles":
        channelName = "Roles"
        channelType = len(guild.roles)
        cont = True
      if messagecontent == prefix + "addcounter messages":
        channelName = "Messages"
        count = 0

        #loading message
        embed = discord.Embed(color=0x593695)
        embed.add_field(name="@" + client.user.name + "#" + client.user.discriminator, value="**Loading...**", inline=False)
        embed.set_footer(text=nowDate + " at " + nowTime)
        message2 = await message.channel.send(embed=embed)

        #get amount of messages
        for channel in guild.text_channels:
          count += len(await channel.history(limit=None).flatten())
        channelType = count
        cont = True

        #store amount of messages
        data["messages"] = count

        await message2.delete()
        
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
      
    #delete counter
    if messagecontent.startswith(prefix + "delcounter"):
      for channel in message.guild.voice_channels:
        try: 
          if channel.name.lower().startswith(str(messagecontent.split()[1])):
            await channel.delete()
        except:
          break 

    #check bump disboard
    if messagecontent == '!d bump':
      bumped = True
      #get user (member object)
      user = message.author
    #check disboard bot reply
    elif bumped == True:
      if str(message.author.id) == "302050872383242240": #disboard bot ID
        if str(message.embeds[0].colour) == "#24b7b7":
          data[str(user.id)]['bumps'] += 1
      bumped = False

    #disboard bumps
    if messagecontent.startswith(prefix + 'd bumps'):
      #get user (member object)
      if (messagecontent == prefix + 'd bumps'):
        user = message.author
      else:
        user = message.guild.get_member(message.mentions[0].id)

      #change database
      bumps = data[str(user.id)]['bumps']

      #send embed
      embed = discord.Embed(color=0x593695, description="User has bumped the server **" + str(bumps) + "** times!")
      embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar_url)
      embed.set_footer(text=nowDate + " at " + nowTime)
      await message.channel.send(embed=embed)

    #help invites (InviteManager)
    if messagecontent == prefix + 'help invites':
      embed = discord.Embed(color=0x593695)
      embed.set_author(name=client.user.name + " Invites Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "invites [member]`", value="Shows how many invites the user has", inline=False)
      embed.add_field(name="`"+prefix+ "leaderboard`", value="Shows the invites leaderboard", inline=False)
      embed.add_field(name="`"+prefix+ "edit <invites|leaves> <amount> [member]`", value="Set invites or leaves of a user", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help reactions (Zira)
    if messagecontent == prefix + 'help reactions':
      embed = discord.Embed(color=0x593695)
      embed.set_author(name=client.user.name + " Reactions Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "rr <channelID> <messageID> <reaction> <role>`", value="Give a role when user reacts to message", inline=False)
      embed.add_field(name="`"+prefix+ "delrr <channelID> <messageID>`", value="Remove a reaction role", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help stats (Server Stats)
    if messagecontent == prefix + 'help counters':
      embed = discord.Embed(color=0x593695)
      embed.set_author(name=client.user.name + " Counters Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "addcounter <tracker>`", value="Make a new server counter", inline=False)
      embed.add_field(name="`"+prefix+ "delcounter <tracker>`", value="Delete a server counter", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help commands
    if messagecontent == prefix + 'help commands':
      embed = discord.Embed(color=0x593695)
      embed.set_author(name=client.user.name + " Commands Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "database`", value="Retrieve past info and store in database", inline=False)
      embed.add_field(name="`"+prefix+ "info [member]`", value="Show info about a member", inline=False)
      embed.add_field(name="`"+prefix+ "prefix <prefix>`", value="Change the command prefix", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help disboard
    if messagecontent == prefix + 'help disboard':
      embed = discord.Embed(color=0x593695)
      embed.set_author(name=client.user.name + " Disboard Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "d leaderboard`", value="Show the disboard bump leaderboard", inline=False)
      embed.add_field(name="`"+prefix+ "d bumps [member]`", value="Show how many bumps a user has", inline=False)
      embed.add_field(name="`"+prefix+ "edit bumps <amount> [member]`", value="Set bumps of a member", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)
    
    #change prefix
    if messagecontent.startswith(prefix + 'prefix '):
      data["prefix"] = messagecontent.split()[1]
      await client.change_presence(activity=discord.Streaming(name=" | " + data["prefix"] + "help", url="https://www.twitch.tv/xzennara/about"))

    #only run on guild_id server
    if messagecontent.startswith(prefix + 'invites') and str(message.guild.id) == guild_id:
      #get user (member object)
      if (messagecontent == prefix + 'invites'):
        user = message.author
      else:
        user = message.guild.get_member(message.mentions[0].id)

      #check if user is in database
      Invites = data[str(user.id)]['invites']
      Leaves = data[str(user.id)]['leaves']
      totalInvites = Invites - Leaves

      embed = discord.Embed(color=0x593695, description="User has **" + str(totalInvites) + "** invites! (**" + str(Invites) + "** regular, **-" + str(Leaves) + "** leaves)")
      embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar_url)
      embed.set_footer(text=nowDate + " at " + nowTime)

      await message.channel.send(embed=embed)

    if messagecontent.startswith(prefix + 'info'):
        #get user (member object)
        if (messagecontent == prefix + 'info'):
          user = message.author
        else:
          user = message.guild.get_member(message.mentions[0].id)

        #set embed
        embed = discord.Embed(color=0x593695)
        embed.set_author(name="@" + user.name + "#" + user.discriminator)
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
  await asyncio.sleep(1.1)

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
  await asyncio.sleep(1.1)

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
client.loop.create_task(checkCounters())

keep_alive.keep_alive() 
#keep the bot running after the window closes, use UptimeRobot to ping the website at least every <60min. to prevent the website from going to sleep, turning off the bot

#run bot
#Bot token is in .env file on repl.it, which isn't viewable by data
client.run(os.environ.get("TOKEN"))