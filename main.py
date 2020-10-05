#CastleMiner Discord bot, made by Zennara#8377
#This is a custom discord bot. It is written to work on only one server.

#imports
import keep_alive
import discord
import os
import asyncio
import json
from datetime import datetime
import math

#declare client
client = discord.Client()

#server-specific ids
guild_id = "566984586618470411"
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

async def incorrectServer(message):
  embed = discord.Embed(color=0x593695, description="Command not available in " + message.guild.name + ".")
  embed.set_author(name="❌ | @" + client.user.name)
  await message.channel.send(embed=embed)

async def incorrectRank(message):
  embed = discord.Embed(color=0x593695, description="insufficient role in the server heirarchy.")
  embed.set_author(name="❌ | @" + client.user.name)
  await message.channel.send(embed=embed)

def checkRole(message, data):
  if message.author.top_role >= message.guild.get_role(int(data["admin" + str(message.guild.id)]['role'])) or message.author == message.guild.owner or message.author.id == "427968672980533269":
    return True
  else:
    return False

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
async def on_raw_reaction_add(payload):
  with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()
  #make sure its not initial reaction
  if payload.member != client.user:
    #check if key exists in database
    if "role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id) in data:
      #check if it is correct reaction emoji
      if str(payload.emoji.name) == str(data["role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id)]['reaction']):
        #give role
        role = payload.member.guild.get_role(int(data["role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id)]['role']))
        await payload.member.add_roles(role, atomic=True)

@client.event
async def on_raw_reaction_remove(payload):
  with open("database.json", 'r') as f:
    data = json.load(f)
    f.close()
  if "role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id) in data:
    #check if it is correct reaction emoji
    if str(payload.emoji.name) == str(data["role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id)]['reaction']):
      #give role
      role = client.get_guild(int(payload.guild_id)).get_role(int(data["role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id)]['role']))
      await client.get_guild(int(payload.guild_id)).get_member(payload.user_id).remove_roles(role, atomic=True)

@client.event
async def on_message(message):
    global user
    global bumped
    #get prefix
    with open("database.json", 'r') as f:
      data = json.load(f)
      f.close()
    prefix = data["prefix"]

    if str(message.guild.id) == guild_id:
      #get messages and add
      data["messages"] += 1

    #set message content to lowercase
    messagecontent = message.content.lower()

    #split current datetime
    nowDT = str(datetime.now()).split()
    nowDate = nowDT[0]
    nowTime = str(datetime.strptime(str(nowDT[1][0 : len(nowDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))

    if str(message.guild.id) == guild_id: 
      #put users in database
      if str(message.guild.id) + str(message.author.id) not in data:
        data[str(message.guild.id) + str(message.author.id)] = {'server': str(message.guild.id), 'name': str(message.author.name) + "#" + str(message.author.discriminator), 'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}

      try:
        if str(message.guild.id) + str(message.guild.get_member(message.mentions[0].id).id) not in data:
          data[str(message.guild.id) + str(message.guild.get_member(message.mentions[0].id).id)] = {'server': str(message.guild.id), 'name': str(message.guild.get_member(message.mentions[0].id).name) + "#" + str(message.guild.get_member(message.mentions[0].id).discriminator), 'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
      except:
        pass

    #setup server
    if messagecontent == prefix + "setup":
      if str(message.guild.id) == guild_id:
        if message.author == message.guild.owner or str(message.author.id) == "427968672980533269" :
          if "admin" + str(message.guild.id) not in data:
            #loading message
            embed = discord.Embed(color=0x593695, description="**Loading Users Into Database...**")
            embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            message2 = await message.channel.send(embed=embed)
            #members
            for member in message.guild.members:
              #add member to database
              if str(message.guild.id) + str(member.id) not in data:
                data[str(message.guild.id) + str(member.id)] = {'server': str(message.guild.id), 'name': str(member.name) + "#" + str(member.discriminator), 'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}

            #invites
            embed = discord.Embed(color=0x593695, description="**Loading Previous Invites**")
            embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message2.edit(embed=embed)
            for member in message.guild.members:
              totalInvites = 0
              for i in await message.guild.invites():
                if i.inviter == member:
                  totalInvites += i.uses
              data[str(message.guild.id) + str(member.id)]['invites'] = totalInvites

            while True:
              embed = discord.Embed(color=0x593695, description="**Please enter the ID of your Disboard bumping channel.**\nEnter 0 to stop adding channels.")
              embed.set_author(name="📝 | @" + client.user.name, icon_url=client.user.avatar_url)
              embed.set_footer(text=nowDate + " at " + nowTime)
              await message2.edit(embed=embed)

              global done
              global test
              done = False
              def check(m):
                global done
                global test
                #check if user is done inputting channels
                if m.content == "0":
                  done = True
                  passed = True
                else:
                  #define check for disboard bumping channel
                  try:
                    test = message.guild.get_channel(int(m.content))
                    if test != None:
                      passed = True
                    else:
                      passed = False
                  except:
                    passed = False
                return passed == True and m.channel == message.channel

              #wait for user input
              msg = await client.wait_for('message', check=check)

              #check if user is done inputting channels
              if done:
                break

              #disboard bumps
              embed = discord.Embed(color=0x593695, description="**Loading Previous Disboard Bumps**\nThis could take a while.")
              embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar_url)
              embed.set_footer(text=nowDate + " at " + nowTime)
              await message2.edit(embed=embed)
              bumped = False
              bumpedAuthor = ""
              for messages in await test.history(limit=None, oldest_first=True).flatten():
                #check if previous message was bump
                if bumped == True:
                  #check if bump was from Disboard bot
                  if str(messages.author.id) == str(messages.guild.id) + "302050872383242240": #disboard bot ID
                    #check if succesful bump (blue color)
                    if str(messages.embeds[0].colour) == "#24b7b7":
                      data[str(message.guild.id) + str(bumpedAuthor)]['bumps'] += 1
                  bumped = False  
                #check if message was bump
                if messages.content == "!d bump":
                  bumped = True
                  bumpedAuthor = message.author.id

            #code admin role
            embed = discord.Embed(color=0x593695, description="**Please enter the ID of the lowest role in the hierarchy able to do server-managing bot commands.**")
            embed.set_author(name="📝 | @" + client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message2.edit(embed=embed)

            def check(m):
              #define check for role
              try:
                test = message.guild.get_role(int(m.content))
                if test != None:
                  passed = True
                else:
                  passed = False
              except:
                passed = False
              return passed == True and m.channel == message.channel

            msg = await client.wait_for('message', check=check)

            #write to data
            data["admin" + str(message.guild.id)] = {"server": str(message.guild.id), "role": str(msg.content)}

            embed = discord.Embed(color=0x593695, description="**" + str(message.guild.name) + " Setup Complete**")
            embed.set_author(name="✔️ | @" + client.user.name, icon_url=client.user.avatar_url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message2.edit(embed=embed)
          else:
            embed = discord.Embed(color=0x593695, description="**Setup has already been completed.**")
            embed.set_author(name="❌ | @" + client.user.name)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message.channel.send(embed=embed)
        else:
          await incorrectRank(message)
      else:
        await incorrectServer(message)

    #fetch invites bumps
    if messagecontent == prefix + "fetch invites":
      def check(reaction, user):
        return user == message.author and str(reaction.emoji) == '✔️'

      embed = discord.Embed(color=0x593695, description="**WARNING: Doing so may result in data loss. Continue?**\nReact with ✅ or wait 30s")
      embed.set_author(name="❔ | @" + client.user.name, icon_url=client.user.avatar_url)
      embed.set_footer(text=nowDate + " at " + nowTime)
      message2 = await message.channel.send(embed=embed)
      await message2.add_reaction('✅')

      try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
      except asyncio.TimeoutError:
        await message2.delete()
      else:
        #invites
        embed = discord.Embed(color=0x593695, description="**Loading Previous Invites**")
        embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar_url)
        embed.set_footer(text=nowDate + " at " + nowTime)
        await message2.edit(embed=embed)
        for member in message.guild.members:
          totalInvites = 0
          for i in await message.guild.invites():
            if i.inviter == member:
              totalInvites += i.uses
          data[str(message.guild.id) + str(member.id)]['invites'] = totalInvites

        embed = discord.Embed(color=0x593695, description="**Previous Invites Fetched**")
        embed.set_author(name="✔️ | @" + client.user.name, icon_url=client.user.avatar_url)
        embed.set_footer(text=nowDate + " at " + nowTime)
        await message2.edit(embed=embed)

    #add code admin
    if messagecontent.startswith(prefix + "codeadmin"):
      if checkRole(message, data):
        try:
          #get role
          codeRole = message.guild.get_role(int(messagecontent.split()[1]))

          #write to database
          data["admin" + str(message.guild.id)] = {"server": str(message.guild.id), "role": str(codeRole.id)}

          #print embed
          embed = discord.Embed(color=0x593695, description="All members with the role " + codeRole.mention + " and higher can use code admin commands.")
          embed.set_author(name="✔️ | @" + client.user.name)
          await message.channel.send(embed=embed)
        except:
          pass
      else:
        await incorrectRank(message)

    #add invite role
    if messagecontent.startswith(prefix + "addirole"):
      if str(message.guild.id) == guild_id:
        if checkRole(message, data):
          try:
            #get data
            content = messagecontent.split()
            iCount = int(content[1])
            iRole = message.guild.get_role(int(content[2]))

            #save to data
            if "irole" + str(message.guild.id) + str(iRole.id) not in data:
              data['irole' + str(message.guild.id) + str(iRole.id)] = {"server": str(message.guild.id), "amount": int(iCount), "roleID": str(iRole.id)}

              #print embed
              embed = discord.Embed(color=0x593695, description="Invite role-reward added.")
              embed.set_author(name="✔️ | @" + client.user.name)
              await message.channel.send(embed=embed)
            else:
              embed = discord.Embed(color=0x593695, description="Role already used")
              embed.set_author(name="❌ | @" + client.user.name)
              await message.channel.send(embed=embed)
          except:
            pass
        else:
          await incorrectRank(message)
      else:
        await incorrectServer(message)
      
    #delete invite role
    if messagecontent.startswith(prefix + "delirole"):
      if str(message.guild.id) == guild_id:
        if checkRole(message, data):
          try:
            #getdata
            deliRole = message.guild.get_role(int(messagecontent.split()[1]))

            if "irole" + str(message.guild.id) + str(deliRole.id) in data:
              #delete key
              del data["irole" + str(message.guild.id) + str(deliRole.id)]

              #print embed
              embed = discord.Embed(color=0x593695, description="Invite role-reward deleted.")
              embed.set_author(name="✔️ | @" + client.user.name)
              await message.channel.send(embed=embed)
            else:
              embed = discord.Embed(color=0x593695, description="Invite role-reward does not exist.")
              embed.set_author(name="❌ | @" + client.user.name)
              await message.channel.send(embed=embed)
          except:
            pass
        else:
          await incorrectRank(message)
      else:
        await incorrectServer(message)

    #show all invite role-rewards
    if messagecontent == prefix + "iroles":
      if str(message.guild.id) == guild_id:
        #get all RR messages
        count = 0
        embed = discord.Embed(color=0x593695, description="**Invite Role-Rewards**")
        for k in data.keys():
          if k.startswith('irole'):
            count += 1
            embed.add_field(name="Reward "+str(count), value="**Role:** <@&" + str(data[k]['roleID']) + ">\n**Invites:** " + str(data[k]['amount']))

        embed.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
        embed.set_footer(text=nowDate + " at " + nowTime)
        await message.channel.send(embed=embed) 
      else:
        await incorrectServer(message)

    #invite leaderboard
    if messagecontent.startswith(prefix + "leaderboard"):
      if str(message.guild.id) == guild_id:
        #make new dictionary to sort
        tempdata = {}
        for key in data.keys():
          if not key.startswith('role') and not key.startswith('irole') and not key.startswith('admin')and key != "prefix" and key != "messages" and key.startswith(str(message.guild.id)):
            tempdata[key] = data[key]['invites'] - data[key]['leaves']
        #sort data
        order = sorted(tempdata.items(), key=lambda x: x[1], reverse=True)

        #get page number
        page = 1
        page = int(page)
        try:
          page = messagecontent.split()[1]
          page = int(page)
        except:
          pass

        if int(page) >= 1 and int(page) <= math.ceil(len(message.guild.members) / 10):
          #store all the users in inputText to later print
          inputText = ""
          count = 1
          for i in order:
            if count <= page * 10 and count >= page * 10 - 9:
              try:
                inputText += "\n`[" + str(count) +"]` **" + str(message.guild.get_member(int(i[0][18:])).name) + "** - **" + str(i[1]) + "** invites (**" + str(data[i[0]]['invites']) + "** regular, **-" + str(data[i[0]]['leaves']) + "** leaves)"
              except:
                inputText += "\n`[" + str(count) +"]` **" + str(data[str(message.guild.id) + str(i[0][18:])]['name'])[:-5] + "** - **" + str(i[1]) + "** invites (**" + str(data[str(message.guild.id) + str(i[0][18:])]['invites']) + "** regular, **-" + str(data[str(message.guild.id) + str(i[0][18:])]['leaves']) + "** leaves)"
            count += 1

          #print embed
          embed = discord.Embed(color=0x593695, description=inputText)
          embed.set_footer(text="Page " + str(page) + "/" + str(math.ceil(len(message.guild.members) / 10)) + " ● " + nowDate + " at " + nowTime)
          embed.set_author(name="Invite Leaderboard", icon_url=message.guild.icon_url) 
          await message.channel.send(embed=embed)
      else:
        await incorrectServer(message)  

    #disboard bump leaderboard
    if messagecontent.startswith(prefix + "d leaderboard"):
      if str(message.guild.id) == guild_id:
        #make new dictionary to sort
        tempdata = {}
        for key in data.keys():
          if not key.startswith('role') and not key.startswith('irole') and not key.startswith('admin') and key != "prefix" and key != "messages" and key.startswith(str(message.guild.id)):
            tempdata[key] = data[key]['bumps']
        #sort data
        order = sorted(tempdata.items(), key=lambda x: x[1], reverse=True)

        #get page number
        try:
          page = messagecontent.split()[2]
        except:
          page = 1

        if int(page) >= 1 and int(page) <= math.ceil(len(message.guild.members) / 10) and str(page).isdigit():
          #store all the users in inputText to later print
          inputText = ""
          count = 1
          for i in order:
            if count <= page * 10 and count >= page * 10 - 9:
              try:
                inputText += "\n`[" + str(count) +"]` **" + str(message.guild.get_member(int(i[0][18:])).name) + "** - **" + str(i[1]) + "** bumps"
              except:
                inputText += "\n`[" + str(count) +"]` **" + str(data[str(message.guild.id) + str(i[0][18:])]) + "** - **" + str(i[1]) + "** bumps"
            count += 1

          #print embed
          embed = discord.Embed(color=0x593695, description=inputText)
          embed.set_footer(text="Page " + str(page) + "/" + str(math.ceil(len(message.guild.members) / 10)) + " ● " + nowDate + " at " + nowTime)
          embed.set_author(name="Disboard Bumps Leaderboard", icon_url=message.guild.icon_url) 
          await message.channel.send(embed=embed)
      else:
        await incorrectServer(message)
      

    #delete rr
    if messagecontent.startswith(prefix + "delrr"):
      if checkRole(message, data):
        try:
          #get messageID
          channelID = messagecontent.split()[1]
          messageID = messagecontent.split()[2]

          #get channel, message, role
          for channel in message.guild.channels:
            if str(channel.id) == str(channelID):
              channel2 = channel
              break
          msg = await channel2.fetch_message(int(messageID))

          #delete role
          if "role" + str(message.guild.id) + str(channelID) + str(messageID) in data:
            await msg.remove_reaction(data["role" + str(message.guild.id) + str(channelID) + str(messageID)]['reaction'], client.user)
            del data["role" + str(message.guild.id) + str(channelID) + str(messageID)]

            #print embed
            embed = discord.Embed(color=0x593695, description="Role reaction message deleted.")
            embed.set_author(name="✔️ | @" + client.user.name)
            await message.channel.send(embed=embed)
          else:
            embed = discord.Embed(color=0x593695, description="Role reaction message doesnt exist.")
            embed.set_author(name="❌ | @" + client.user.name)
            await message.channel.send(embed=embed)
        except:
          pass
      else:
        await incorrectRank(message)

    if messagecontent == prefix + "reactions":  
      #display all role reaction messages
      embed = discord.Embed(color=0x593695, description="**Messages with Reaction Roles**")

      #get all invite role rewards
      count = 0
      for k in data.keys():
        if k.startswith('role'):
          count += 1
          embed.add_field(name="Message "+str(count), value="**Role:** <@&" + str(data[k]['role']) + ">\n**Emoji:** " + str(data[k]['reaction']) + "\n**Channel: ** <#" + str(data[k]['channel']) + ">\n**Message ID:** " + str(data[k]['message']) + "[\nJump to message](https://discordapp.com/channels/"+str(message.guild.id)+"/"+str(data[k]['channel'])+"/"+str(data[k]['message'])+")")

      #print embed
      embed.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
      embed.set_footer(text=nowDate + " at " + nowTime)
      await message.channel.send(embed=embed)

    #add role reaction message
    if messagecontent.startswith(prefix + 'rr'):
      if checkRole(message, data):
        try:
          #get variables
          sCont = messagecontent.split()
          RRchannelID = sCont[1]
          RRmessageID = sCont[2]
          RRreaction = sCont[3]
          RRroleID = sCont[4]

          #get channel, message
          for channel in message.guild.channels:
            if str(channel.id) == str(RRchannelID):
              channel2 = channel
              break
          msg = await channel2.fetch_message(int(RRmessageID))

          #add to data
          if "role" + str(channel2.id) + str(msg.id) not in data:
            role = message.guild.get_role(int(RRroleID))
            roleID = role.id
            #give starter reaction
            await msg.add_reaction(RRreaction)
            placement = "role" + str(message.guild.id) + str(channel2.id) + str(msg.id)
            data[placement] = {'server': str(message.guild.id), 'channel': str(RRchannelID), 'message': str(RRmessageID), 'reaction': RRreaction, 'role': str(roleID)}

            #print embed
            embed = discord.Embed(color=0x593695, description="Role reaction message added.")
            embed.set_author(name="✔️ | @" + client.user.name)
            await message.channel.send(embed=embed)
          else:
            embed = discord.Embed(color=0x593695, description="Role reaction message already exists.")
            embed.set_author(name="❌ | @" + client.user.name)
            await message.channel.send(embed=embed)
        except:
          pass
      else:
        await incorrectRank(message)

    #edit amounts
    if messagecontent.startswith(prefix + "edit"):
      if str(message.guild.id) == guild_id:
        if checkRole(message, data):
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
            prevAmount = data[str(user.guild.id) + str(user.id)][str(editType)]

            editAmount = int(messagecontent.split()[2])

            if editType == "invites" or editType == "leaves" or editType == "bumps":
              data[str(user.guild.id) + str(user.id)][str(editType)] = editAmount

              #send embed
              embed = discord.Embed(color=0x593695, description="User now has **" + str(editAmount) + "** " + editType + "!" + " (Original: **" + str(prevAmount) + "**)")
              embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar_url)
              embed.set_footer(text=nowDate + " at " + nowTime)
              await message.channel.send(embed=embed)
          except:
            pass
        else:
          await incorrectRank(message)
      else:
        await incorrectServer(message)

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

    if messagecontent.startswith(prefix + "addcounter"):
      #add counter
      if str(message.guild.id) == guild_id:
        if checkRole(message, data):
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
            embed.add_field(name="⌛ | @" + client.user.name, value="**Loading...**", inline=False)
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

              #print embed
              embed = discord.Embed(color=0x593695, description=channelName + " counter added.")
              embed.set_author(name="✔️ | @" + client.user.name)
              await message.channel.send(embed=embed)
            else:
              embed = discord.Embed(color=0x593695, description=channelName + " counter already exists.")
              embed.set_author(name="❌ | @" + client.user.name)
              await message.channel.send(embed=embed)
        else:
          await incorrectRank(message)
      else:
        await incorrectServer(message)
      
    #delete counter
    if messagecontent.startswith(prefix + "delcounter"):
      if str(message.guild.id) == guild_id: 
        if checkRole(message, data):
          for channel in message.guild.voice_channels:
            try: 
              if channel.name.lower().startswith(str(messagecontent.split()[1])):
                await channel.delete()
            except:
              break 
        else:
          await incorrectRank(message)
      else:
        await incorrectServer(message)

    #check bump disboard
    if messagecontent == '!d bump':
      bumped = True
      #get user (member object)
      user = message.author
    #check disboard bot reply
    elif bumped == True:
      if str(message.guild.id) + str(message.author.id) == str(message.guild.id) + "302050872383242240": #disboard bot ID
        if str(message.embeds[0].colour) == "#24b7b7":
          data[str(user.guild.id) + str(user.id)]['bumps'] += 1
      bumped = False

    #disboard bumps
    if messagecontent.startswith(prefix + 'd bumps'):
      if str(message.guild.id) == guild_id: 
        #get user (member object)
        if (messagecontent == prefix + 'd bumps'):
          user = message.author
        else:
          user = message.guild.get_member(message.mentions[0].id)

        #change database
        bumps = data[str(user.guild.id) + str(user.id)]['bumps']

        #send embed
        embed = discord.Embed(color=0x593695, description="User has bumped the server **" + str(bumps) + "** times!")
        embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar_url)
        embed.set_footer(text=nowDate + " at " + nowTime)
        await message.channel.send(embed=embed)
      else:
        await incorrectServer(message)

    #help invites (InviteManager)
    if messagecontent == prefix + 'help invites':
      embed = discord.Embed(color=0x593695)
      embed.set_author(name=client.user.name + " Invites Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "invites [member]`", value="Shows how many invites the user has", inline=False)
      embed.add_field(name="`"+prefix+ "leaderboard`", value="Shows the invites leaderboard", inline=False)
      embed.add_field(name="`"+prefix+ "edit <invites|leaves> <amount> [member]`", value="Set invites or leaves of a user", inline=False)
      embed.add_field(name="`"+prefix+ "addirole <invites> <roleID>`", value="Add a new invite role reward", inline=False)
      embed.add_field(name="`"+prefix+ "delirole <invites> <roleID>`", value="Delete an invite role reward", inline=False)
      embed.add_field(name="`"+prefix+ "iroles`", value="Display all invite role rewards", inline=False)
      embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
      await message.channel.send(embed=embed)

    #help reactions (Zira)
    if messagecontent == prefix + 'help reactions':
      embed = discord.Embed(color=0x593695)
      embed.set_author(name=client.user.name + " Reactions Help", icon_url=client.user.avatar_url)
      embed.add_field(name="`"+prefix+ "rr <channelID> <messageID> <:reaction:> <roleID>`", value="Give a role when user reacts to message", inline=False)
      embed.add_field(name="`"+prefix+ "delrr <channelID> <messageID>`", value="Remove a reaction role", inline=False)
      embed.add_field(name="`"+prefix+ "reactions`", value="Lists all role reaction messages", inline=False)
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
      embed.add_field(name="`"+prefix+ "setup`", value="Setup the server", inline=False)
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
      if checkRole(message, data):
        data["prefix"] = messagecontent.split()[1]
        await client.change_presence(activity=discord.Streaming(name=" | " + data["prefix"] + "help", url="https://www.twitch.tv/xzennara/about"))
      else:
        await incorrectRank(message)

    #only run on guild_id server
    if messagecontent.startswith(prefix + 'invites'):
      if str(message.guild.id) == guild_id: 
        #get user (member object)
        if (messagecontent == prefix + 'invites'):
          user = message.author
        else:
          user = message.guild.get_member(message.mentions[0].id)

        #check if user is in database
        Invites = data[str(user.guild.id) + str(user.id)]['invites']
        Leaves = data[str(user.guild.id) + str(user.id)]['leaves']
        totalInvites = Invites - Leaves

        embed = discord.Embed(color=0x593695, description="User has **" + str(totalInvites) + "** invites! (**" + str(Invites) + "** regular, **-" + str(Leaves) + "** leaves)")
        embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar_url)
        embed.set_footer(text=nowDate + " at " + nowTime)

        await message.channel.send(embed=embed)
      else:
        await incorrectServer(message)

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
          jCode = data[str(user.guild.id) + str(user.id)]['joinCode']

          embed.add_field(name="Join Code", value=jCode, inline=True)
          if data[str(user.guild.id) + str(user.id)]['inviter'] != "null":
            inviterMember = message.guild.get_member(int(data[str(user.guild.id) + str(user.id)]['inviter']))
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

  if str(member.guild.id) == guild_id: 
    #append join code
    if str(member.guild.id) + str(member.id) not in data:
      data[str(member.guild.id) + str(member.id)] = {'server': str(member.guild.id), 'name': str(member.name) + "#" + str(member.discriminator), 'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': joinCode, 'inviter': codeOwner}
    data[str(member.guild.id) + str(member.id)]['joinCode'] = joinCode
    data[str(member.guild.id) + str(member.id)]['inviter'] = codeOwner

    #add to invites
    if str(member.guild.id) + codeOwner not in data:
      data[str(member.guild.id) + codeOwner] = {'server': str(member.guild.id), 'name': str(member.guild.get_member(int(codeOwner)).name) + "#" + str(member.guild.get_member(int(codeOwner)).discriminator), 'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null", 'inviter': "null"}
    data[str(member.guild.id) + codeOwner]['invites'] += 1
  
  #check for iroles
  for key in data.keys():
    #check for irole keys
    if key.startswith('irole'):
      #check codeowner invites
      if data[str(member.guild.id) + data[str(member.guild.id) + str(member.id)]['inviter']]['invites'] - data[str(member.guild.id) + data[str(member.guild.id) + str(member.id)]['inviter']]['leaves'] >= data[key]['amount']:
        #give role
        await member.guild.get_member(int(data[str(member.guild.id) + str(member.id)]['inviter'])).add_roles((member.guild.get_role(int(data[key]['roleID']))), atomic=True)

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

  if str(member.guild.id) == guild_id:
    #add to leaves
    if str(member.guild.id) + str(member.id) in data:
      if data[str(member.guild.id) + str(member.id)]['inviter'] != "null":
        data[str(member.guild.id) + data[str(member.guild.id) + str(member.id)]['inviter']]['leaves'] += 1

  #check for iroles
  for key in data.keys():
    #check for irole keys
    if key.startswith('irole'):
      #check codeowner invites
      if data[str(member.guild.id) + data[str(member.guild.id) + str(member.id)]['inviter']]['invites'] - data[str(member.guild.id) + data[str(member.guild.id) + str(member.id)]['inviter']]['leaves'] < data[key]['amount']:
        #remove role
        await member.guild.get_member(int(codeOwner)).remove_roles((member.guild.get_role(int(data[key]['roleID']))), atomic=True)

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