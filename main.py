# CastleMiner Discord bot, made by Zennara#8377
# This is a custom discord bot. It is written to work on only one server.

# imports
import discord
import os
import asyncio
import json
from datetime import datetime
import math
import requests
import random
from discord import Webhook
import aiohttp
import json
from discord.ext import tasks

# declare client
intents = discord.Intents.all()
client = discord.Client(intents=intents)


# json config data
f = open('config.json', encoding="utf-8")  # open json file
config = json.load(f)  # load file into dict
f.close()  # close file


# server-specific ids
guild_id = str(config["guild_id"])
guild = client.get_guild(int(guild_id))
# print(data["566984586618470411434547908415586311"]["invites"])


# database functions
data = {}


# function to re-read data again from json database
def read_data():
    f = open('database.json', encoding="utf-8")  # open json
    global data
    data = json.load(f)  # read data
    f.close()  # close


# function to write json data
def write_data(data):
    # Serializing json
    json_object = json.dumps(data, indent=2)

    # Writing to sample.json
    with open("database.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_object)


read_data()


def update_data():
    global data
    read_data()
    write_data(data)


# delete database
CLEAR = False
if CLEAR:
    count = 0
    for key in data:
        del data[key]
        count += 1
        print(count)
    update_data()

# dump data in database.json
DUMP = False
if DUMP:
    data2 = {}
    count = 0
    for key in data:
        data2[str(key)] = data[str(key)]
        count += 1
        print(str(count))

    with open("database.json", 'w') as f:
        json.dump(str(data2), f)

DBFIX = True
if DBFIX:
    # data["admin684524717167607837"] = {"server": "684524717167607837", "role": "684535492619927587"}
    data["prefix"] = "cm/"

invites = {}


@client.event
async def on_invite_create(invite):
    # write cache
    invites[invite.guild.id] = await invite.guild.invites()


@client.event
async def on_invite_delete(invite):
    # write cache
    invites[invite.guild.id] = await invite.guild.invites()


# check invites and compare
# invites = {}
# last = ""
# async def getInvites():
#  global last
#  global invites
#  global codeOwner
#  global joinCode
#  await client.wait_until_ready()
#  gld = client.get_guild(int(guild_id))
#  while True:
#    invs = await gld.invites()
#    tmp = []
#    for i in invs:
#      for s in invites:
#        if s[0] == i.code:
#          if int(i.uses) > s[1]:
#            #get inviter id
#            codeOwner = str(i.inviter.id)
#            joinCode = str(i.code)
#      tmp.append(tuple((i.code, i.uses)))
#    invites = tmp
#  await asyncio.sleep(1)

@tasks.loop(seconds = 10) # repeat after every 10 seconds
async def checkCounters():
    while True:
        # discord API limits rates to twice every 10m for channel edits
        await asyncio.sleep(600)

        # update channels
        for guild in client.guilds:
            # steam
            header = {"Client-ID": "F07D7ED5C43A695B3EBB01C28B6A18E5"}
            game_players_url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid='
            # get amount of bots
            bots = 0
            for member in guild.members:
                if member.bot:
                    bots += 1
            for channel in guild.voice_channels:
                if channel.name.startswith("Members"):
                    if (channel.name != "Members: " + str(guild.member_count - bots)):
                        await channel.edit(name="Members: " + str(guild.member_count - bots))
                if channel.name.startswith("Bots"):
                    if (channel.name != "Bots: " + str(bots)):
                        await channel.edit(name="Bots: " + str(bots))
                if channel.name.startswith("Channels"):
                    if (channel.name != "Channels: " + str(
                            len(guild.text_channels) + len(guild.voice_channels) - len(guild.categories))):
                        await channel.edit(name="Channels: " + str(
                            len(guild.text_channels) + len(guild.voice_channels) - len(guild.categories)))
                if channel.name.startswith("Text Channels"):
                    if (channel.name != "Text Channels: " + str(len(guild.text_channels))):
                        await channel.edit(name="Text Channels: " + str(len(guild.text_channels)))
                if channel.name.startswith("Voice Channels"):
                    if (channel.name != "Voice Channels: " + str(len(guild.voice_channels))):
                        await channel.edit(name="Voice Channels: " + str(len(guild.voice_channels)))
                if channel.name.startswith("Categories"):
                    if (channel.name != "Categories: " + str(len(guild.categories))):
                        await channel.edit(name="Categories: " + str(len(guild.categories)))
                if channel.name.startswith("Roles"):
                    if (channel.name != "Roles: " + str(len(guild.roles))):
                        await channel.edit(name="Roles: " + str(len(guild.roles)))
                if channel.name.startswith("Bans"):
                    if (channel.name != "Bans: " + str(len(await guild.bans()))):
                        await channel.edit(name="Bans: " + str(len(await guild.bans())))
                if channel.name.startswith("Messages"):
                    if (channel.name != "Messages: " + str(data['messages'])):
                        await channel.edit(name="Messages: " + str(data['messages']))
                if channel.name.startswith("CMZ Players"):
                    game_players = requests.get(game_players_url + "253430", headers=header)
                    if (channel.name != "CMZ Players: " + str(game_players.json()['response']['player_count'])):
                        await channel.edit(name="CMZ Players: " + str(game_players.json()['response']['player_count']))
                if channel.name.startswith("CMW Players"):
                    game_players = requests.get(game_players_url + "675210", headers=header)
                    if (channel.name != "CMW Players: " + str(game_players.json()['response']['player_count'])):
                        await channel.edit(name="CMW Players: " + str(game_players.json()['response']['player_count']))


# header = {"Client-ID": "F07D7ED5C43A695B3EBB01C28B6A18E5"}
# appIDs = ["253430", "675210", "414550"]
# game_players = [0,0,0]
# for i in range(0, 3):
#  game_players_url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid=' + appIDs[i]
#  game_players[i] = requests.get(game_players_url, headers=header)

# print("CMZ: " + str(game_players[0].json()['response']['player_count']))
# print("CMW: " + str(game_players[1].json()['response']['player_count']))
# print("Death Toll: " + str(game_players[2].json()['response']['player_count']))

def find_invite_by_code(invite_list, code):
    # Simply looping through each invite in an
    # invite list which we will get using guild.invites()
    for inv in invite_list:
        # Check if the invite code in this element
        # of the list is the one we're looking for
        if inv.code == code:
            # If it is, we return it.
            return inv


async def incorrectServer(message):
    embed = discord.Embed(color=0x593695, description="Command not available in " + message.guild.name + ".")
    embed.set_author(name="❌ | @" + client.user.name)
    await message.channel.send(embed=embed)


async def incorrectRank(message):
    embed = discord.Embed(color=0x593695, description="insufficient role in the server heirarchy.")
    embed.set_author(name="❌ | @" + client.user.name)
    await message.channel.send(embed=embed)


def checkRole(message, data):
    if message.author.top_role >= message.guild.get_role(
            int(data["admin" + str(message.guild.id)]['role'])) or message.author == message.guild.owner or str(
            message.author.id) == "427968672980533269":
        return True
    else:
        return False


@client.event
async def on_ready():
    global bumped
    bumped = False
    print("\nZennInvites Ready\n")
    await client.change_presence(
        activity=discord.Streaming(name=" | " + data["prefix"] + "help", url="https://www.twitch.tv/xzennara/about"))

    # Getting all the guilds our bot is in
    for guild in client.guilds:
        # Adding each guild's invites to our dict
        invites[guild.id] = await guild.invites()

    # gg = client.get_guild(566984586618470411)
    # for ban in await gg.bans():
    #  if ban.user.name.lower().startswith("scatman"):
    #    print(f"{ban.user.id} | {ban.user.name}")

    await checkCounters.start()


# channel and category IDs restricted for starboard
noStarboard = ["591135975355187200", "759976154479984650", "572774759331397632", "706953196425314820",
               "738634279357251586", "812692775895957574"]


@client.event
async def on_raw_reaction_add(payload):
    # STARBOARD
    # check not restricted category
    guild = client.get_guild(int(guild_id))
    channel = guild.get_channel(payload.channel_id)
    starchannel = guild.get_channel(812692775895957574)
    if str(channel.category.id) not in noStarboard and str(channel.id) not in noStarboard:
        # check for star
        if payload.emoji.name == "⭐":
            message = await channel.fetch_message(payload.message_id)
            count = {react.emoji: react.count for react in message.reactions}
            print(count)
            # check star count
            if count['⭐'] >= 6:
                # check msg already in starchannel
                done = False
                async for msg in starchannel.history(limit=None):
                    if msg.content.startswith(message.jump_url):
                        done = True
                if not done:
                    embed = discord.Embed(color=0xFFD700, description=message.content)
                    embed.set_author(name=message.author.name + "#" + message.author.discriminator,
                                     icon_url=message.author.avatar.url)
                    # get all files
                    files = []
                    for ach in message.attachments:
                        files.append(await ach.to_file())
                    # get all non-link embeds
                    doEmbeds = True
                    for emb in message.embeds:
                        if str(emb.provider) != "EmbedProxy()":
                            doEmbeds = False
                    # define webhook
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(config["starboard_webhook_url"], session=session)
                        await webhook.send(username=message.author.display_name, avatar_url=message.author.avatar.url,
                                           content=message.jump_url + "\n\n" + message.content, files=files)
                        # if all non-link embeds
                        if doEmbeds:
                            try:
                                await webhook.send(username=message.author.name, avatar_url=message.author.avatar.url,
                                                   embeds=message.embeds)
                            except:
                                pass

    # make sure its not initial reaction
    if payload.member != client.user:
        # check if key exists in database
        if "role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id) in data:
            # check if it is correct reaction emoji
            if str(payload.emoji.name) == str(
                    data["role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id)][
                        'reaction']):
                # give role
                role = payload.member.guild.get_role(int(
                    data["role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id)]['role']))
                await payload.member.add_roles(role, atomic=True)


@client.event
async def on_raw_reaction_remove(payload):
    if "role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id) in data:
        # check if it is correct reaction emoji
        if str(payload.emoji.name) == str(
                data["role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id)]['reaction']):
            # give role
            role = client.get_guild(int(payload.guild_id)).get_role(
                int(data["role" + str(payload.guild_id) + str(payload.channel_id) + str(payload.message_id)]['role']))
            await client.get_guild(int(payload.guild_id)).get_member(int(payload.user_id)).remove_roles(role,
                                                                                                        atomic=True)


@client.event
async def on_member_update(before, after):
    # anti zalgo etc
    percentbad = 0
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 `+_-~=[]\\{}|;:\"\',<.>/?!@#$%^&*()"
    if before.nick != after.nick:
        for char in after.nick:
            if char not in characters:
                percentbad += 1
        percentbad = (percentbad / len(after.nick)) * 100
        if percentbad > 50:
            await after.edit(nick=before.nick)
            embed = discord.Embed(color=0x593695,
                                  description="Can not change nickname. Contains more that 50 percent of non-allowed characters. Please only use the standard english keyboard.")
            embed.set_author(name="❌ | @" + client.user.name)
            await after.send(embed=embed)


@client.event
async def on_message(message):
    global user
    global bumped
    # get prefix
    prefix = data["prefix"]

    # if str(message.guild.id) == guild_id:
    # get messages and add
    # data["messages"] += 1

    # set message content to lowercase
    messagecontent = message.content.lower().replace('<', '').replace('>', '').replace('!', '').replace('#',
                                                                                                        '').replace('@',
                                                                                                                    '').replace(
        '&', '')

    # split current datetime
    nowDT = str(datetime.now()).split()
    nowDate = nowDT[0]
    nowTime = str(datetime.strptime(str(nowDT[1][0: len(nowDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))

    if str(message.guild.id) == guild_id:
        # put users in database
        if str(message.author.id) not in data:
            data[str(message.author.id)] = {'server': str(message.guild.id),
                                            'name': str(message.author.name) + "#" + str(message.author.discriminator),
                                            'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null",
                                            'inviter': "null"}

        try:
            if str(message.guild.get_member(message.mentions[0].id).id) not in data:
                data[str(message.guild.get_member(message.mentions[0].id).id)] = {'server': str(message.guild.id),
                                                                                  'name': str(message.guild.get_member(
                                                                                      message.mentions[
                                                                                          0].id).name) + "#" + str(
                                                                                      message.guild.get_member(
                                                                                          message.mentions[
                                                                                              0].id).discriminator),
                                                                                  'invites': 0, 'leaves': 0, 'bumps': 0,
                                                                                  'joinCode': "null", 'inviter': "null"}
        except:
            pass

    # grab for-digitaldna
    if messagecontent == prefix + "grab memos":
        if checkRole(message, data):
            guild = client.get_guild(int(guild_id))
            forddna = message.guild.get_channel(671495633051451397)
            messageData = {}
            # loop through messages in channel
            async for m in forddna.history(limit=None):
                # write content
                messageData[str(m.author.id)] = {"name": str(m.author.name + "#" + m.author.discriminator),
                                                 "content": m.content,
                                                 "pfp": str(m.author.avatar.url)}
            # load to json
            obj = json.dumps(messageData, indent=4)
            with open("For_DDNA_Responses.json", "w") as outfile:
                outfile.write(obj)

            # generate file
            file = discord.File("For_DDNA_Responses.json")

            # send message
            await message.channel.send("**Below is the** `.json`** file of all the responses in** " + forddna.mention,
                                       file=file)
        else:
            await incorrectRank(message)

    # grab signatures
    if messagecontent == prefix + "grab signatures":
        if checkRole(message, data):
            guild = client.get_guild(int(guild_id))
            sigs = message.guild.get_channel(933608307170623498)
            messageData = {}
            # loop through messages in channel
            async for m in sigs.history(limit=None):
                # write content
                if m.attachments:  # check if there is attachment
                    messageData[str(m.author.id)] = {"name": m.author.name + "#" + m.author.discriminator,
                                                     "signature": str(m.attachments[0].url)}
                else:  # no attachments
                    messageData[str(m.author.id)] = {"name": m.author.name + "#" + m.author.discriminator,
                                                     "signature": m.content}
            # load to json
            obj = json.dumps(messageData, indent=4)
            with open("Signatures.json", "w") as outfile:
                outfile.write(obj)

            # generate file
            file = discord.File("Signatures.json")

            # send message
            await message.channel.send("**Below is the** `.json`** file of all the signatures in** " + sigs.mention,
                                       file=file)
        else:
            await incorrectRank(message)

    # fake ban
    if messagecontent.startswith(prefix + "ban"):
        if checkRole(message, data):
            memberName = message.guild.get_member(int(messagecontent.split()[1])).mention
            embed = discord.Embed(color=0x593695, description=memberName + "*** has been banned! F.***")
            embed.set_author(name="✔️ | @" + client.user.name)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message.channel.send(embed=embed)
        else:
            await incorrectRank(message)

    # custom message
    if messagecontent.startswith(prefix + "custom"):
        if checkRole(message, data):
            embed = discord.Embed(color=0x593695, description=str(messagecontent.split(maxsplit=1)[1]))
            embed.set_author(name="✔️ | @" + client.user.name)
            embed.set_footer(
                text="Made by " + message.author.name + "#" + message.author.discriminator + "\n" + nowDate + " at " + nowTime)
            await message.channel.send(embed=embed)
            await message.delete()
        else:
            await incorrectRank(message)

    # giveaway
    if messagecontent.startswith(prefix + "giveaway"):
        if checkRole(message, data):
            try:
                channel = message.guild.get_channel(int(messagecontent.split()[1]))
                event = await channel.fetch_message(int(messagecontent.split()[2]))
                reaction = event.reactions[0]

                users = await reaction.users().flatten()
                # users is now a list of User...
                winner = random.choice(users)
                await message.channel.send(':cupcake: ***{}***  **has won the giveaway!**'.format(winner))
            except:
                embed = discord.Embed(color=0x593695, description="Invalid Syntax")
                embed.set_author(name="❌ | @" + client.user.name)
                embed.set_footer(text=nowDate + " at " + nowTime)
                await message.channel.send(embed=embed)
        else:
            await incorrectRank(message)

    # cross
    if messagecontent == prefix + "cross":
        server = 0
        count = 0
        i = 0
        players = [""]
        # main server
        if message.guild.id == 566984586618470411:
            server = 684524717167607837
        # modding
        if message.guild.id == 684524717167607837:
            server = 566984586618470411

        embed = discord.Embed(color=0x593695, description="")

        for member in message.guild.members:
            if member not in client.get_guild(server).members:
                if message.guild.id == 566984586618470411:
                    memberName = str(member.name) + "#" + str(member.discriminator)
                else:
                    memberName = str(member.mention)
                players[i] += "`" + str(count + 1) + " |` " + memberName + "\n";
                count += 1
                if count >= 50 * (i + 1):
                    players.append("")
                    embed.description = players[i]
                    embed.set_author(name="✔️ | @" + client.user.name)
                    await message.channel.send(embed=embed)
                    i += 1
        embed.description = players[i]
        embed.set_author(name="✔️ | @" + client.user.name)
        await message.channel.send(embed=embed)

        embed.description = "**" + str(count) + " members not in " + client.get_guild(
            server).name + "**\n*Offline members may not tag correctly*"
        embed.set_author(name="✔️ | @" + client.user.name)
        embed.set_footer(text=nowDate + " at " + nowTime)
        await message.channel.send(embed=embed)
        print(count)

        # if len(players) == 1:
        # embed.add_field(name="1", value=str(players[0]))

    # setup server
    if messagecontent == prefix + "setup":
        if str(message.guild.id) == guild_id:
            if message.author == message.guild.owner or str(message.author.id) == "427968672980533269":
                if "admin" + str(message.guild.id) not in data:
                    # loading message
                    embed = discord.Embed(color=0x593695, description="**Loading Users Into Database...**")
                    embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar.url)
                    embed.set_footer(text=nowDate + " at " + nowTime)
                    message2 = await message.channel.send(embed=embed)
                    # members
                    for member in message.guild.members:
                        # add member to database
                        if str(member.id) not in data:
                            data[str(member.id)] = {'server': str(message.guild.id),
                                                    'name': str(member.name) + "#" + str(member.discriminator),
                                                    'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null",
                                                    'inviter': "null"}
                        await asyncio.sleep(0.1)

                    # invites
                    embed = discord.Embed(color=0x593695, description="**Loading Previous Invites**")
                    embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar.url)
                    embed.set_footer(text=nowDate + " at " + nowTime)
                    await message2.edit(embed=embed)
                    for member in message.guild.members:
                        totalInvites = 0
                        for i in await message.guild.invites():
                            if i.inviter == member:
                                totalInvites += i.uses
                        tmp = data[str(member.id)];
                        del data[str(member.id)]
                        tmp['invites'] = totalInvites
                        data[str(member.id)] = tmp
                        update_data()

                    while True:
                        embed = discord.Embed(color=0x593695,
                                              description="**Please enter the ID of your Disboard bumping channel.**\nEnter 0 to stop adding channels.")
                        embed.set_author(name="📝 | @" + client.user.name, icon_url=client.user.avatar.url)
                        embed.set_footer(text=nowDate + " at " + nowTime)
                        await message2.edit(embed=embed)

                        global done
                        global test
                        done = False

                        def check(m):
                            global done
                            global test
                            # check if user is done inputting channels
                            if m.content == "0":
                                done = True
                                passed = True
                            else:
                                # define check for disboard bumping channel
                                try:
                                    test = message.guild.get_channel(int(m.content))
                                    if test != None:
                                        passed = True
                                    else:
                                        passed = False
                                except:
                                    passed = False
                            return passed == True and m.channel == message.channel

                        # wait for user input
                        msg = await client.wait_for('message', check=check)

                        # check if user is done inputting channels
                        if done:
                            break

                        # disboard bumps
                        embed = discord.Embed(color=0x593695,
                                              description="**Loading Previous Disboard Bumps**\nThis could take a while.")
                        embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar.url)
                        embed.set_footer(text=nowDate + " at " + nowTime)
                        await message2.edit(embed=embed)
                        bumped = False
                        bumpedAuthor = ""
                        for messages in await test.history(limit=None, oldest_first=True).flatten():
                            # check if previous message was bump
                            if bumped == True:
                                # check if bump was from Disboard bot
                                if str(messages.author.id) == "302050872383242240":  # disboard bot ID
                                    # check if succesful bump (blue color)
                                    if str(messages.embeds[0].colour) == "#24b7b7":
                                        if str(bumpedAuthor.id) not in data:
                                            data[str(bumpedAuthor.id)] = {'server': str(message.guild.id),
                                                                          'name': str(bumpedAuthor.name) + "#" + str(
                                                                              bumpedAuthor.discriminator), 'invites': 0,
                                                                          'leaves': 0, 'bumps': 0, 'joinCode': "null",
                                                                          'inviter': "null"}
                                        tmp = data[str(bumpedAuthor.id)]
                                        del data[str(bumpedAuthor.id)]
                                        tmp['bumps'] += 1
                                        data[str(bumpedAuthor.id)] = tmp
                                        update_data()
                                bumped = False
                            # check if message was bump
                            if messages.content == "!d bump":
                                bumped = True
                                bumpedAuthor = messages.author

                    # code admin role
                    embed = discord.Embed(color=0x593695,
                                          description="**Please enter the ID of the lowest role in the hierarchy able to do server-managing bot commands.**")
                    embed.set_author(name="📝 | @" + client.user.name, icon_url=client.user.avatar.url)
                    embed.set_footer(text=nowDate + " at " + nowTime)
                    await message2.edit(embed=embed)

                    def check(m):
                        # define check for role
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

                    # write to data
                    data["admin" + str(message.guild.id)] = {"server": str(message.guild.id), "role": str(msg.content)}

                    embed = discord.Embed(color=0x593695,
                                          description="**" + str(message.guild.name) + " Setup Complete**")
                    embed.set_author(name="✔️ | @" + client.user.name, icon_url=client.user.avatar.url)
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

    # poll
    if message.content.startswith(prefix + "poll"):
        numemojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        try:
            msg = message.content.split("\"")

            await message.delete()

            count = 0
            print(len(msg))
            if len(msg) > 3:
                options = ""
                for i in range(len(msg)):
                    if i > 1 and i % 2 != 0:
                        options = options + "\n" + numemojis[count] + " " + msg[i]
                        count += 1
            else:
                options = ""

            embed = discord.Embed(color=0x593695, description="**📊 | " + msg[1] + "**\n\n" + options)
            embed.set_footer(text=nowDate + " at " + nowTime)
            pollmsg = await message.channel.send(embed=embed)

            if len(msg) < 4:
                await pollmsg.add_reaction('👍')
                await pollmsg.add_reaction('👎')
            else:
                for i in range(0, int((len(msg) - 3) / 2)):
                    await pollmsg.add_reaction(numemojis[i])

        except:
            embed = discord.Embed(color=0x593695,
                                  description="**Invalid Poll Usage**\nRefer to syntax at cm/help polls")
            embed.set_author(name="❌ | @" + client.user.name, icon_url=client.user.avatar.url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message.channel.send(embed=embed)

    # reports
    if messagecontent == prefix + "report":
        def check(m):
            if (message.author.id == m.author.id and m.guild == None):
                return True
            else:
                return False

        async def reportmsg():
            embed = discord.Embed(color=0x593695,
                                  description="**Report started**\nUse cm/cancel in DM to cancel the report.")
            embed.set_author(name="✅ | @" + client.user.name, icon_url=client.user.avatar.url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message.author.send(embed=embed)

            embed = discord.Embed(color=0x593695, description="**In-game name of attacker:**")
            embed.set_author(name="📝 | @" + client.user.name, icon_url=client.user.avatar.url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            message2 = await message.author.send(embed=embed)
            inGameName = await client.wait_for('message', check=check)
            if inGameName.content == "cm/cancel":
                print("test123")
                return

            embed.description = "**Steam Name or Link:**\nType *NA* if unavailable."
            await message2.edit(embed=embed)
            steamName = await client.wait_for('message', check=check)
            if steamName.content == "cm/cancel":
                return

            embed.description = "**Discord Name and Tag:**\nType *NA* if unavailable."
            await message2.edit(embed=embed)
            discordName = await client.wait_for('message', check=check)
            if discordName.content == "cm/cancel":
                return

            embed.description = "**What game did the event take place?**"
            await message2.edit(embed=embed)
            game = await client.wait_for('message', check=check)
            if game.content == "cm/cancel":
                return

            embed.description = "**Description of the event:**"
            await message2.edit(embed=embed)
            description = await client.wait_for('message', check=check)
            if description.content == "cm/cancel":
                return

            embed.description = "**Were you using a mod?**\nIf so, which one?"
            await message2.edit(embed=embed)
            modName = await client.wait_for('message', check=check)
            if modName.content == "cm/cancel":
                return

            embed = discord.Embed(color=0x593695, description="**Thank you for your report.**")
            embed.set_author(name="✅ | @" + client.user.name, icon_url=client.user.avatar.url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message2.edit(embed=embed)

            embed = discord.Embed(color=0x593695,
                                  description="**IGN: **" + inGameName.content + "\n**Steam: **" + steamName.content + "\n**Discord: **" + discordName.content)
            embed.add_field(name="Game", value=game.content)
            embed.add_field(name="Mod", value=modName.content)
            embed.add_field(name="Description", value=description.content, inline=False)
            embed.set_author(name="✖ | @" + client.user.name, icon_url=client.user.avatar.url)
            embed.set_footer(
                text=nowDate + " at " + nowTime + "\nReport by: " + message.author.name + "#" + message.author.discriminator)
            await message.author.send(embed=embed)

            if "report" in data:
                channel = message.guild.get_channel(int(data["report"]["channel"]))
                await channel.send(embed=embed)
            else:
                embed = discord.Embed(color=0x593695,
                                      description="**Failed to send report**\nContact an admin if you think this is a mistake.")
                embed.set_author(name="❌ | @" + client.user.name, icon_url=client.user.avatar.url)
                embed.set_footer(text=nowDate + " at " + nowTime)
                await message2.edit(embed=embed)

        await reportmsg()

    # create report channel
    if messagecontent.startswith(prefix + "reportchannel"):
        if checkRole(message, data):
            try:
                # get role
                reportChannel = message.guild.get_channel(int(messagecontent.split()[1]))

                # write to database
                if "report" in data:
                    del data["report"]
                data["report"] = {"server": str(message.guild.id), "channel": str(reportChannel.id)}
                update_data()

                # print embed
                embed = discord.Embed(color=0x593695, description="Reports will now go to " + reportChannel.mention)
                embed.set_author(name="✔️ | @" + client.user.name)
                await message.channel.send(embed=embed)
            except:
                pass
        else:
            await incorrectRank(message)

    # fetch invites
    if messagecontent == prefix + "fetch invites":
        if str(message.guild.id) == guild_id:
            if checkRole(message, data):
                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) == '✅'

                embed = discord.Embed(color=0x593695,
                                      description="**WARNING: Doing so may result in data loss. Continue?**\nReact with ✅ or wait 30s")
                embed.set_author(name="❔ | @" + client.user.name, icon_url=client.user.avatar.url)
                embed.set_footer(text=nowDate + " at " + nowTime)
                message2 = await message.channel.send(embed=embed)
                await message2.add_reaction('✅')

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await message2.delete()
                else:
                    # invites
                    embed = discord.Embed(color=0x593695, description="**Loading Previous Invites**")
                    embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar.url)
                    embed.set_footer(text=nowDate + " at " + nowTime)
                    await message2.edit(embed=embed)
                    count = 0
                    for member in message.guild.members:
                        totalInvites = 0
                        if str(member.id) not in data:
                            data[str(member.id)] = {'server': str(message.guild.id),
                                                    'name': str(member.name) + "#" + str(member.discriminator),
                                                    'invites': 0, 'leaves': 0, 'bumps': 0, 'joinCode': "null",
                                                    'inviter': "null"}
                        count += 1
                        print("member passed | " + str(member.id) + " | " + str(count));
                        for i in await message.guild.invites():
                            if i.inviter == member:
                                totalInvites += i.uses
                        try:
                            tmp = data[str(member.id)]
                            del data[str(member.id)]
                            tmp['invites'] = totalInvites
                            data[str(member.id)] = tmp
                            update_data()
                        except:
                            embed = discord.Embed(color=0x593695, description="<@!" + str(member.id) + ">")
                            embed.set_author(name="❌ | @" + client.user.name, icon_url=client.user.avatar.url)
                            embed.set_footer(text=nowDate + " at " + nowTime)
                            await message.channel.send(embed=embed)

                    embed = discord.Embed(color=0x593695, description="**Previous Invites Fetched**")
                    embed.set_author(name="✔️ | @" + client.user.name, icon_url=client.user.avatar.url)
                    embed.set_footer(text=nowDate + " at " + nowTime)
                    await message2.edit(embed=embed)
            else:
                await incorrectRank(message)
        else:
            await incorrectServer(message)

    # fetch disboard bumps
    if messagecontent == prefix + "fetch bumps":
        if str(message.guild.id) == guild_id:
            tmp2 = {}
            tmp2 = dict(data)
            if checkRole(message, data):
                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) == '✅'

                embed = discord.Embed(color=0x593695,
                                      description="**WARNING: Doing so may result in data loss. Continue?**\nReact with ✅ or wait 30s")
                embed.set_author(name="❔ | @" + client.user.name, icon_url=client.user.avatar.url)
                embed.set_footer(text=nowDate + " at " + nowTime)
                message2 = await message.channel.send(embed=embed)
                await message2.add_reaction('✅')

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await message2.delete()
                else:
                    embed = discord.Embed(color=0x593695, description="**Clearing Bumps...**")
                    embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar.url)
                    embed.set_footer(text=nowDate + " at " + nowTime)
                    await message2.edit(embed=embed)

                    # clear bumps
                    for key in data:
                        try:
                            tmp = data[key]
                            del data[key]
                            tmp['bumps'] = 0
                            data[key] = tmp
                            update_data()
                        except:
                            pass

                    while True:
                        embed = discord.Embed(color=0x593695,
                                              description="**Please enter the ID of your Disboard bumping channel.**\nEnter 0 to stop adding channels.")
                        embed.set_author(name="📝 | @" + client.user.name, icon_url=client.user.avatar.url)
                        embed.set_footer(text=nowDate + " at " + nowTime)
                        await message2.edit(embed=embed)

                        done = False

                        def check(m):
                            global done
                            global test
                            # check if user is done inputting channels
                            if m.content == "0":
                                done = True
                                passed = True
                            else:
                                # define check for disboard bumping channel
                                try:
                                    test = message.guild.get_channel(int(m.content))
                                    if test != None:
                                        passed = True
                                    else:
                                        passed = False
                                except:
                                    passed = False
                            return passed == True and m.channel == message.channel

                        # wait for user input
                        msg = await client.wait_for('message', check=check)

                        # check if user is done inputting channels
                        if done:
                            break

                        # disboard bumps
                        embed = discord.Embed(color=0x593695,
                                              description="**Loading Previous Disboard Bumps**\nThis could take a while.")
                        embed.set_author(name="⌛ | @" + client.user.name, icon_url=client.user.avatar.url)
                        embed.set_footer(text=nowDate + " at " + nowTime)
                        await message2.edit(embed=embed)
                        bumped = False
                        bumpedAuthor = ""
                        for messages in await test.history(limit=None, oldest_first=True).flatten():
                            # check if previous message was bump
                            if bumped == True:
                                # check if bump was from Disboard bot
                                if str(messages.author.id) == "302050872383242240":  # disboard bot ID
                                    # check if succesful bump (blue color)
                                    if str(messages.embeds[0].colour) == "#24b7b7":
                                        if str(bumpedAuthor.id) not in data:
                                            data[str(bumpedAuthor.id)] = {'server': str(message.guild.id),
                                                                          'name': str(bumpedAuthor.name) + "#" + str(
                                                                              bumpedAuthor.discriminator), 'invites': 0,
                                                                          'leaves': 0, 'bumps': 0, 'joinCode': "null",
                                                                          'inviter': "null"}
                                        tmp = data[str(bumpedAuthor.id)]
                                        del data[str(bumpedAuthor.id)]
                                        tmp['bumps'] += 1
                                        data[str(bumpedAuthor.id)] = tmp
                                        update_data()
                                bumped = False
                            # check if message was bump
                            if messages.content == "!d bump":
                                bumped = True
                                bumpedAuthor = messages.author

                    embed = discord.Embed(color=0x593695, description="**Previous Bumps Fetched**")
                    embed.set_author(name="✔️ | @" + client.user.name, icon_url=client.user.avatar.url)
                    embed.set_footer(text=nowDate + " at " + nowTime)
                    await message2.edit(embed=embed)
            else:
                await incorrectRank(message)
        else:
            await incorrectServer(message)

    # add code admin
    if messagecontent.startswith(prefix + "codeadmin"):
        if checkRole(message, data):
            try:
                # get role
                codeRole = message.guild.get_role(int(messagecontent.split()[1]))

                # write to database
                data["admin" + str(message.guild.id)] = {"server": str(message.guild.id), "role": str(codeRole.id)}

                # print embed
                embed = discord.Embed(color=0x593695,
                                      description="All members with the role " + codeRole.mention + " and higher can use code admin commands.")
                embed.set_author(name="✔️ | @" + client.user.name)
                await message.channel.send(embed=embed)
            except:
                pass
        else:
            await incorrectRank(message)

    # add invite role
    if messagecontent.startswith(prefix + "addirole"):
        if str(message.guild.id) == guild_id:
            if checkRole(message, data):
                try:
                    # get data
                    content = messagecontent.split()
                    iCount = int(content[1])
                    iRole = message.guild.get_role(int(content[2]))

                    # save to data
                    if "irole" + str(message.guild.id) + str(iRole.id) not in data:
                        data['irole' + str(message.guild.id) + str(iRole.id)] = {"server": str(message.guild.id),
                                                                                 "amount": int(iCount),
                                                                                 "roleID": str(iRole.id)}

                        # print embed
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

    # delete invite role
    if messagecontent.startswith(prefix + "delirole"):
        if str(message.guild.id) == guild_id:
            if checkRole(message, data):
                try:
                    # getdata
                    deliRole = message.guild.get_role(int(messagecontent.split()[1]))

                    if "irole" + str(message.guild.id) + str(deliRole.id) in data:
                        # delete key
                        del data["irole" + str(message.guild.id) + str(deliRole.id)]
                        update_data()

                        # print embed
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

    # show all invite role-rewards
    if messagecontent == prefix + "iroles":
        if str(message.guild.id) == guild_id:
            # get all RR messages
            count = 0
            embed = discord.Embed(color=0x593695, description="**Invite Role-Rewards**")
            for k in data:
                if k.startswith('irole' + str(message.guild.id)):
                    count += 1
                    embed.add_field(name="Reward " + str(count),
                                    value="**Role:** <@&" + str(data[k]['roleID']) + ">\n**Invites:** " + str(
                                        data[k]['amount']))

            embed.set_author(name=message.guild.name, icon_url=message.guild.icon.url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message.channel.send(embed=embed)
        else:
            await incorrectServer(message)

    # invite leaderboard
    if messagecontent.startswith(prefix + "leaderboard"):
        if str(message.guild.id) == guild_id:
            embed = discord.Embed(color=0x593695, description="Loading . . .\n*This may take up to 25s*")
            embed.set_footer(text="Page " + "?" + "/" + str(
                math.ceil(len(message.guild.members) / 10)) + " ● " + nowDate + " at " + nowTime)
            embed.set_author(name="Invite Leaderboard", icon_url=message.guild.icon.url)
            message2 = await message.channel.send(embed=embed)

            tmp = {}
            tmp = dict(data)
            # make new dictionary to sort
            tempdata = {}
            for key in tmp.keys():
                # all other dataEntries
                if not key.startswith('role') and not key.startswith('irole') and not key.startswith(
                        'admin') and key != "prefix" and key != "messages" and not key.startswith(
                        "report") and not key.startswith("star"):
                    tempdata[key] = tmp[key]['invites'] - tmp[key]['leaves']
            # sort data
            order = sorted(tempdata.items(), key=lambda x: x[1], reverse=True)

            # get page number
            page = 1
            page = int(page)
            try:
                page = messagecontent.split()[1]
                page = int(page)
            except:
                pass

            if int(page) >= 1 and int(page) <= math.ceil(len(message.guild.members) / 10):
                # store all the users in inputText to later print
                inputText = ""
                count = 1
                for i in order:
                    if count <= page * 10 and count >= page * 10 - 9:
                        inputText += "\n`[" + str(count) + "]` <@!" + str(i[0]) + "> - **" + str(
                            i[1]) + "** invites (**" + str(tmp[str(i[0])]['invites']) + "** regular, **-" + str(
                            tmp[str(i[0])]['leaves']) + "** leaves)"
                    count += 1

                # print embed
                embed = discord.Embed(color=0x593695, description=inputText)
                embed.set_footer(text="Page " + str(page) + "/" + str(
                    math.ceil(len(message.guild.members) / 10)) + " ● " + nowDate + " at " + nowTime)
                embed.set_author(name="Invite Leaderboard", icon_url=message.guild.icon.url)
                await message2.edit(embed=embed)
        else:
            await incorrectServer(message)

    # disboard bump leaderboard
    if messagecontent.startswith(prefix + "d leaderboard"):
        if str(message.guild.id) == guild_id:
            embed = discord.Embed(color=0x593695, description="Loading . . .\n*This may take up to 25s*")
            embed.set_footer(text="Page " + "?" + "/" + str(
                math.ceil(len(message.guild.members) / 10)) + " ● " + nowDate + " at " + nowTime)
            embed.set_author(name="Disboard Bumps Leaderboard", icon_url=message.guild.icon.url)
            message2 = await message.channel.send(embed=embed)

            tmp = {}
            tmp = dict(data)
            # make new dictionary to sort
            tempdata = {}
            for key in tmp.keys():
                # all other dataEntries
                if not key.startswith('role') and not key.startswith('irole') and not key.startswith(
                        'admin') and key != "prefix" and key != "messages" and not key.startswith(
                        "report") and not key.startswith("star"):
                    tempdata[key] = tmp[key]['bumps']
            # sort data
            order = sorted(tempdata.items(), key=lambda x: x[1], reverse=True)

            # get page number
            try:
                page = messagecontent.split()[2]
            except:
                page = 1

            if int(page) >= 1 and int(page) <= math.ceil(len(message.guild.members) / 10) and str(page).isdigit():
                # store all the users in inputText to later print
                inputText = ""
                count = 1
                for i in order:
                    if count <= page * 10 and count >= page * 10 - 9:
                        inputText += "\n`[" + str(count) + "]` <@!" + str(i[0]) + "> - **" + str(i[1]) + "** bumps"
                    count += 1

                # print embed
                embed = discord.Embed(color=0x593695, description=inputText)
                embed.set_footer(text="Page " + str(page) + "/" + str(
                    math.ceil(len(message.guild.members) / 10)) + " ● " + nowDate + " at " + nowTime)
                embed.set_author(name="Disboard Bumps Leaderboard", icon_url=message.guild.icon.url)
                await message2.edit(embed=embed)
        else:
            await incorrectServer(message)

    # delete rr
    if messagecontent.startswith(prefix + "delrr"):
        if checkRole(message, data):
            try:
                # get messageID
                channelID = messagecontent.split()[1]
                messageID = messagecontent.split()[2]

                # get channel, message, role
                for channel in message.guild.channels:
                    if str(channel.id) == str(channelID):
                        channel2 = channel
                        break
                msg = await channel2.fetch_message(int(messageID))

                # delete role
                if "role" + str(message.guild.id) + str(channelID) + str(messageID) in data:
                    await msg.remove_reaction(
                        data["role" + str(message.guild.id) + str(channelID) + str(messageID)]['reaction'], client.user)
                    del data["role" + str(message.guild.id) + str(channelID) + str(messageID)]
                    update_data()

                    # print embed
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
        # display all role reaction messages
        embed = discord.Embed(color=0x593695, description="**Messages with Reaction Roles**")

        # get all invite role rewards
        count = 0
        for k in data:
            if k.startswith('role' + str(message.guild.id)):
                count += 1
                embed.add_field(name="Message " + str(count),
                                value="**Role:** <@&" + str(data[k]['role']) + ">\n**Emoji:** " + str(
                                    data[k]['reaction']) + "\n**Channel: ** <#" + str(
                                    data[k]['channel']) + ">\n**Message ID:** " + str(
                                    data[k]['message']) + "[\nJump to message](https://discordapp.com/channels/" + str(
                                    message.guild.id) + "/" + str(data[k]['channel']) + "/" + str(
                                    data[k]['message']) + ")")

        # print embed
        embed.set_author(name=message.guild.name, icon_url=message.guild.icon.url)
        embed.set_footer(text=nowDate + " at " + nowTime)
        await message.channel.send(embed=embed)

    # add role reaction message
    if messagecontent.startswith(prefix + "rr"):
        if checkRole(message, data):
            try:
                # get variables
                sCont = messagecontent.split()
                RRchannelID = sCont[1]
                RRmessageID = sCont[2]
                RRreaction = sCont[3]
                RRroleID = sCont[4]

                # get channel, message
                for channel in message.guild.channels:
                    if str(channel.id) == str(RRchannelID):
                        channel2 = channel
                        break
                msg = await channel2.fetch_message(int(RRmessageID))

                # add to data
                if "role" + str(channel2.id) + str(msg.id) not in data:
                    role = message.guild.get_role(int(RRroleID))
                    roleID = role.id
                    # give starter reaction
                    await msg.add_reaction(RRreaction)
                    placement = "role" + str(message.guild.id) + str(channel2.id) + str(msg.id)
                    data[placement] = {'server': str(message.guild.id), 'channel': str(RRchannelID),
                                       'message': str(RRmessageID), 'reaction': RRreaction, 'role': str(roleID)}

                    # print embed
                    embed = discord.Embed(color=0x593695, description="Role reaction message added.")
                    embed.set_author(name="✔️ | @" + client.user.name)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(color=0x593695, description="Role reaction message already exists.")
                    embed.set_author(name="❌ | @" + client.user.name)
                    await message.channel.send(embed=embed)
            except:
                print("error")
                pass
        else:
            await incorrectRank(message)

    # edit amounts
    if messagecontent.startswith(prefix + "edit"):
        if str(message.guild.id) == guild_id:
            if checkRole(message, data):
                # run in try's in case of error
                # get user (member object)
                try:
                    try:
                        if message.content[-18:].isdigit():
                            user = message.guild.get_member(int(message.content[-18:]))
                        else:
                            user = message.guild.get_member(int(message.content[-19:-1]))
                        test = user.id
                    except:
                        if message.content[-18:].isdigit():
                            user = await client.fetch_user(message.content[-18:])
                        else:
                            user = await client.fetch_user(message.content[-19:-1])
                except:
                    user = message.author
                try:
                    # get type
                    editType = messagecontent.split()[1]

                    # get previous invites amount
                    prevAmount = data[str(user.id)][str(editType)]

                    editAmount = int(messagecontent.split()[2])

                    if editType == "invites" or editType == "leaves" or editType == "bumps":
                        # data[str(message.guild.id) + str(user.id)][str(editType)] = "5"

                        tmp = data[str(user.id)]
                        del data[str(user.id)]
                        tmp[editType] = editAmount
                        data[str(user.id)] = tmp
                        update_data()

                        # send embed
                        embed = discord.Embed(color=0x593695, description="User now has **" + str(
                            editAmount) + "** " + editType + "!" + " (Original: **" + str(prevAmount) + "**)")
                        embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar.url)
                        embed.set_footer(text=nowDate + " at " + nowTime)
                        await message.channel.send(embed=embed)
                except:
                    pass
            else:
                await incorrectRank(message)
        else:
            await incorrectServer(message)

    # help
    if messagecontent == prefix + 'help':
        embed = discord.Embed(color=0x593695)
        embed.set_author(name=client.user.name + " Help", icon_url=client.user.avatar.url)
        start = "`" + prefix + "help"
        embed.add_field(name="Counters", value=start + " counters`", inline=True)
        embed.add_field(name="Invites", value=start + " invites`", inline=True)
        embed.add_field(name="Role Reactions", value=start + " reactions`", inline=True)
        embed.add_field(name="Disboard", value=start + " disboard`", inline=True)
        embed.add_field(name="Reports", value=start + " reports`", inline=True)
        embed.add_field(name="Commands", value=start + " commands`", inline=True)
        embed.set_footer(text="______________________\nMade By Zennara#8377")
        await message.channel.send(embed=embed)

    if messagecontent.startswith(prefix + "addcounter"):
        # add counter
        # here
        if str(message.guild.id) == guild_id:
            if checkRole(message, data):
                guild = client.get_guild(int(guild_id))

                foundCategory = False
                # find category
                for category in guild.categories:
                    if category.name == str(message.guild.name) + " Stats":
                        categoryObject = category
                        foundCategory = True
                        break
                # create category
                if foundCategory == False:
                    categoryObject = await guild.create_category(str(message.guild.name) + " Stats", overwrites=None,
                                                                 reason=None)

                # get amount of bots
                bots = 0
                for member in guild.members:
                    if member.bot:
                        bots += 1

                # get channels/ categories
                total_text_channels = len(guild.text_channels)
                total_voice_channels = len(guild.voice_channels)
                total_channels = total_text_channels + total_voice_channels - len(guild.categories)

                cont = False
                # get channel creation type
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

                    # loading message
                    embed = discord.Embed(color=0x593695)
                    embed.add_field(name="⌛ | @" + client.user.name, value="**Loading...**", inline=False)
                    embed.set_footer(text=nowDate + " at " + nowTime)
                    message2 = await message.channel.send(embed=embed)

                    # get amount of messages
                    for channel in guild.text_channels:
                        count += len(await channel.history(limit=None).flatten())
                    channelType = count
                    cont = True

                    # store amount of messages
                    data["messages"] = count

                    await message2.delete()

                foundChannel = False
                if cont:
                    # find channel
                    for channel in guild.channels:
                        if channel.name.startswith(channelName + ":"):
                            channelObject = channel
                            foundChannel = True
                            break
                    # create channel
                    if foundChannel == False:
                        channelObject = await guild.create_voice_channel(f"{channelName}: {channelType}", category=categoryObject,
                                                                         reason=None)
                        await channelObject.set_permissions(guild.default_role, connect=False)

                        # print embed
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

    # delete counter
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
    # check bump disboard
    if message.content == '!d bump':
        bumped = True
        # get user (member object)
        user = message.author
    # check disboard bot reply
    elif bumped == True:
        if str(message.author.id) == "302050872383242240":  # disboard bot ID
            if str(message.embeds[0].colour) == "#24b7b7":
                tmp = data[str(user.id)]
                del data[str(user.id)]
                tmp['bumps'] += 1
                data[str(user.id)] = tmp
                update_data()
        bumped = False

    # disboard bumps
    if messagecontent.startswith(prefix + 'd bumps'):
        if str(message.guild.id) == guild_id:
            # get user (member object)
            if (messagecontent == prefix + 'd bumps'):
                user = message.author
            else:
                try:
                    if message.content[-18:].isdigit():
                        user = message.guild.get_member(int(message.content[-18:]))
                    else:
                        user = message.guild.get_member(int(message.content[-19:-1]))
                    test = user.id
                except:
                    if message.content[-18:].isdigit():
                        user = await client.fetch_user(message.content[-18:])
                    else:
                        user = await client.fetch_user(message.content[-19:-1])

            # change database
            bumps = data[str(user.id)]['bumps']

            # send embed
            embed = discord.Embed(color=0x593695,
                                  description="User has bumped the server **" + str(bumps) + "** times!")
            embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar.url)
            embed.set_footer(text=nowDate + " at " + nowTime)
            await message.channel.send(embed=embed)
        else:
            await incorrectServer(message)

    # help invites (InviteManager)
    if messagecontent == prefix + 'help invites':
        embed = discord.Embed(color=0x593695)
        embed.set_author(name=client.user.name + " Invites Help", icon_url=client.user.avatar.url)
        embed.add_field(name="`" + prefix + "invites [member]`", value="Shows how many invites the user has",
                        inline=False)
        embed.add_field(name="`" + prefix + "leaderboard`", value="Shows the invites leaderboard", inline=False)
        embed.add_field(name="`" + prefix + "edit <invites|leaves> <amount> [member]`",
                        value="Set invites or leaves of a user", inline=False)
        embed.add_field(name="`" + prefix + "addirole <invites> <roleID>`", value="Add a new invite role reward",
                        inline=False)
        embed.add_field(name="`" + prefix + "delirole <invites> <roleID>`", value="Delete an invite role reward",
                        inline=False)
        embed.add_field(name="`" + prefix + "iroles`", value="Display all invite role rewards", inline=False)
        embed.add_field(name="`" + prefix + "fetch invites`", value="Fetch all previous invites", inline=False)
        embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
        await message.channel.send(embed=embed)

    # help reactions (Zira)
    if messagecontent == prefix + 'help reactions':
        embed = discord.Embed(color=0x593695)
        embed.set_author(name=client.user.name + " Reactions Help", icon_url=client.user.avatar.url)
        embed.add_field(name="`" + prefix + "rr <channelID> <messageID> <:reaction:> <roleID>`",
                        value="Give a role when user reacts to message", inline=False)
        embed.add_field(name="`" + prefix + "delrr <channelID> <messageID>`", value="Remove a reaction role",
                        inline=False)
        embed.add_field(name="`" + prefix + "reactions`", value="Lists all role reaction messages", inline=False)
        embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
        await message.channel.send(embed=embed)

    # help stats (Server Stats)
    if messagecontent == prefix + 'help counters':
        embed = discord.Embed(color=0x593695)
        embed.set_author(name=client.user.name + " Counters Help", icon_url=client.user.avatar.url)
        embed.add_field(name="`" + prefix + "addcounter <tracker>`", value="Make a new server counter", inline=False)
        embed.add_field(name="`" + prefix + "delcounter <tracker>`", value="Delete a server counter", inline=False)
        embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
        await message.channel.send(embed=embed)

    # help commands
    if messagecontent == prefix + 'help commands':
        embed = discord.Embed(color=0x593695)
        embed.set_author(name=client.user.name + " Commands Help", icon_url=client.user.avatar.url)
        embed.add_field(name="`" + prefix + "setup`", value="Setup the server", inline=False)
        embed.add_field(name="`" + prefix + "info [member]`", value="Show info about a member", inline=False)
        embed.add_field(name="`" + prefix + "prefix <prefix>`", value="Change the command prefix", inline=False)
        embed.add_field(name="`" + prefix + "codeadmin <roleID>`", value="Change the admin rank ID", inline=False)
        embed.add_field(name="`" + prefix + "poll <\"desc\"> [\"option\"]`", value="Create a poll.", inline=False)
        embed.add_field(name="`" + prefix + "cross`", value="Returns list of members not in the other server.",
                        inline=False)
        embed.add_field(name="`" + prefix + "ban <member>`", value="Fake-bans this member.", inline=False)
        embed.add_field(name="`" + prefix + "giveaway <channel> <message>`",
                        value="Selects a random winner from that message reactions.", inline=False)
        embed.add_field(name="`" + prefix + "custom <message>`", value="Sends a custom embed message.", inline=False)
        embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
        await message.channel.send(embed=embed)

    # help disboard
    if messagecontent == prefix + 'help disboard':
        embed = discord.Embed(color=0x593695)
        embed.set_author(name=client.user.name + " Disboard Help", icon_url=client.user.avatar.url)
        embed.add_field(name="`" + prefix + "d leaderboard`", value="Show the disboard bump leaderboard", inline=False)
        embed.add_field(name="`" + prefix + "d bumps [member]`", value="Show how many bumps a user has", inline=False)
        embed.add_field(name="`" + prefix + "edit bumps <amount> [member]`", value="Set bumps of a member",
                        inline=False)
        embed.add_field(name="`" + prefix + "fetch bumps`", value="Fetch all previous bumps", inline=False)
        embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
        await message.channel.send(embed=embed)

    # help reports
    if messagecontent == prefix + 'help reports':
        embed = discord.Embed(color=0x593695)
        embed.set_author(name=client.user.name + " Reports Help", icon_url=client.user.avatar.url)
        embed.add_field(name="`" + prefix + "report`", value="Start a report", inline=False)
        embed.add_field(name="`" + prefix + "reportchannel`", value="Changes the reports channel", inline=False)
        embed.set_footer(text="________________________\n<> Required | [] Optional\nMade By Zennara#8377")
        await message.channel.send(embed=embed)

    # change prefix
    if messagecontent.startswith(prefix + 'prefix '):
        if checkRole(message, data):
            tmp = data["prefix"]
            del data["prefix"]
            tmp = messagecontent.split()[1]
            data["prefix"] = tmp
            update_data()
            await client.change_presence(activity=discord.Streaming(name=" | " + data["prefix"] + "help",
                                                                    url="https://www.twitch.tv/xzennara/about"))
        else:
            await incorrectRank(message)

    # only run on guild_id server
    if messagecontent.startswith(prefix + 'invites'):
        if str(message.guild.id) == guild_id:
            # get user (member object)
            if (messagecontent == prefix + 'invites'):
                user = message.author
            else:
                try:
                    if message.content[-18:].isdigit():
                        user = message.guild.get_member(int(message.content[-18:]))
                    else:
                        user = message.guild.get_member(int(message.content[-19:-1]))
                    test = user.id
                except:
                    if message.content[-18:].isdigit():
                        user = await client.fetch_user(message.content[-18:])
                    else:
                        user = await client.fetch_user(message.content[-19:-1])

            # check if user is in database
            Invites = data[str(user.id)]['invites']
            Leaves = data[str(user.id)]['leaves']
            totalInvites = Invites - Leaves

            embed = discord.Embed(color=0x593695,
                                  description="User has **" + str(totalInvites) + "** invites! (**" + str(
                                      Invites) + "** regular, **-" + str(Leaves) + "** leaves)")
            embed.set_author(name="@" + user.name + "#" + str(user.discriminator), icon_url=user.avatar.url)
            embed.set_footer(text=nowDate + " at " + nowTime)

            await message.channel.send(embed=embed)
        else:
            await incorrectServer(message)

    if messagecontent.startswith(prefix + 'info'):
        # get user (member object)
        if (messagecontent == prefix + 'info'):
            user = message.author
            joinedDT = str(user.joined_at).split()
            joinedDate = joinedDT[0] + " at "
            joinedTime = str(
                datetime.strptime(str(joinedDT[1][0: len(joinedDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))
        else:
            try:
                if message.content[-18:].isdigit():
                    user = message.guild.get_member(int(message.content[-18:]))
                else:
                    user = message.guild.get_member(int(message.content[-19:-1]))
                # split joined_at into date and time
                joinedDT = str(user.joined_at).split()
                joinedDate = joinedDT[0] + " at "
                joinedTime = str(
                    datetime.strptime(str(joinedDT[1][0: len(joinedDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))
            except:
                if message.content[-18:].isdigit():
                    user = await client.fetch_user(message.content[-18:])
                else:
                    user = await client.fetch_user(message.content[-19:-1])
                joinedDate = "No longer in the server."
                joinedTime = ""

        # set embed
        embed = discord.Embed(color=0x593695)
        embed.set_author(name="@" + user.name + "#" + user.discriminator)
        embed.add_field(name="ID:", value=user.id, inline=False)
        embed.set_thumbnail(url=user.avatar.url)

        # split created_at into date and time
        createDT = str(user.created_at).split()
        createdDate = createDT[0]
        createdTime = str(datetime.strptime(str(createDT[1][0: len(createDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))

        embed.add_field(name="Joined Server at", value=joinedDate + joinedTime, inline=False)

        # join code and owner, only run on guild_id server
        if str(message.guild.id) == guild_id:
            jCode = data[str(user.id)]['joinCode']

            embed.add_field(name="Join Code", value=jCode, inline=True)
            if data[str(user.id)]['inviter'] != "null":
                inviterMember = str(data[str(user.id)]['inviter'])
                if inviterMember in data:
                    embed.add_field(name="Owned By", value=data[inviterMember]['name'], inline=True)
                else:
                    embed.add_field(name="Owned By", value="<@!" + inviterMember + ">", inline=True)

        # joined discord
        embed.add_field(name="Joined Discord at", value=createdDate + " at " + createdTime, inline=False)

        try:
            # if boosting display since when
            if (str(user.premium_since) != "None"):
                # split premium_since into date and time
                premiumDT = str(user.premium_since).split()
                premiumDate = premiumDT[0]
                premiumTime = str(
                    datetime.strptime(str(premiumDT[1][0: len(premiumDT[1]) - 7]), "%H:%M:%S").strftime("%I:%M %p"))
                embed.add_field(name="Boosting Server since", value=premiumDate + " at " + premiumTime, inline=False)
        except:
            pass

        # requested by
        embed.set_footer(
            text="Requested by " + message.author.name + "#" + message.author.discriminator + "\nID: " + str(
                message.author.id))
        await message.channel.send(embed=embed)


@client.event
async def on_member_join(member):
    global last
    global lastName
    last = str(member.id)
    lastName = str(member.name)

    # wait until getInvites() is done
    await asyncio.sleep(1.1)

    if str(member.guild.id) == guild_id:
        invites_before_join = invites[member.guild.id]
        invites_after_join = await member.guild.invites()
        for invite in invites_before_join:
            if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
                gotInvite = invite
                # print(f"Member {member.name} Joined")
                # print(f"Invite Code: {invite.code}")
                # print(f"Inviter: {invite.inviter}")
                invites[member.guild.id] = invites_after_join
                break

        # write cache
        invites[member.guild.id] = await member.guild.invites()

        # append join code
        if str(member.id) not in data:
            data[str(member.id)] = {'server': str(member.guild.id),
                                    'name': str(member.name) + "#" + str(member.discriminator), 'invites': 0,
                                    'leaves': 0, 'bumps': 0, 'joinCode': gotInvite.code,
                                    'inviter': str(gotInvite.inviter.id)}

        tmp = data[str(member.id)]
        del data[str(member.id)]
        tmp['joinCode'] = gotInvite.code
        data[str(member.id)] = tmp

        tmp = data[str(member.id)]
        del data[str(member.id)]
        tmp['inviter'] = str(gotInvite.inviter.id)
        data[str(member.id)] = tmp

        # add to invites
        if str(gotInvite.inviter.id) not in data:
            data[str(gotInvite.inviter.id)] = {'server': str(member.guild.id), 'name': str(
                member.guild.get_member(int(gotInvite.inviter.id)).name) + "#" + str(
                member.guild.get_member(int(gotInvite.inviter.id)).discriminator), 'invites': 0, 'leaves': 0,
                                               'bumps': 0, 'joinCode': "null", 'inviter': "null"}
        tmp = data[str(gotInvite.inviter.id)]
        del data[str(gotInvite.inviter.id)]
        tmp['invites'] += 1
        data[str(gotInvite.inviter.id)] = tmp
        update_data()

    # check for iroles
    for key in data:
        # check for irole keys
        if key.startswith('irole'):
            # check codeowner invites
            if data[data[str(member.id)]['inviter']]['invites'] - data[data[str(member.id)]['inviter']]['leaves'] >= \
                    data[key]['amount']:
                # give role
                await member.guild.get_member(int(data[str(member.id)]['inviter'])).add_roles(
                    (member.guild.get_role(int(data[key]['roleID']))), atomic=True)

    # anti zalgo etc
    percentbad = 0
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 `+_-~=[]\\{}|;:\"\',<.>/?!@#$%^&*()"
    for char in member.name:
        if char not in characters:
            percentbad += 1
    percentbad = (percentbad / len(member.name)) * 100
    if percentbad > 50:
        await member.edit(nick="NEEDSCHANGED")


@client.event
async def on_member_remove(member):
    # write cache
    invites[member.guild.id] = await member.guild.invites()

    if str(member.guild.id) == guild_id:
        # add to leaves
        if str(member.id) in data:
            if data[str(member.id)]['inviter'] != "null":
                tmp = data[data[str(member.id)]['inviter']]
                del data[data[str(member.id)]['inviter']]
                tmp['leaves'] += 1
                data[data[str(member.id)]['inviter']] = tmp
                update_data()

    # check for iroles
    for key in data:
        # check for irole keys
        if key.startswith('irole'):
            # check codeowner invites
            codeOwner = data[str(member.id)]['inviter']
            if int(data[data[str(member.id)]['inviter']]['invites']) - int(
                    data[data[str(member.id)]['inviter']]['leaves']) < int(data[key]['amount']):
                update_data()
                # remove role
                await member.guild.get_member(int(codeOwner)).remove_roles(
                    (member.guild.get_role(int(data[key]['roleID']))), atomic=True)

# run bot
client.run(config["Token"])
