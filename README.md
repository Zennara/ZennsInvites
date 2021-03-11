# ZennDev
A discord bot developed in Python3 along with the Discord.py API after InviteManager, a discord bot, was regulated by Discord. This bot is for personal use by the [CastleMiner Discord](discord.gg/cJH7DFb) Server.
[![Run on Repl.it](https://repl.it/badge/github/Zennara/ZennsInvites)](https://repl.it/github/Zennara/ZennsInvites)
## Invite Manager
These sets of features add the ability to track each member who joins and leaves the server, carefully logging the code they used to join, who owned that code, and adding invites/leaves to the owner of that code. It also has the ability to reward and take away roles at specified invite amounts. 
## Roles on Message Reactions
ZennDev also offers features including awarded roles when a user reacts to a specific message with a specific role. This are also intended to be a lot easier to set up then Zira's time consuming process. 
## Server Stats
Channels can also be added displaying different stats of the current server. These include; members, bots, channels, textchannels, voicechannels, categories, roles, bans, and messages.
## Disboard Bot Integration
ZennDev is able to track bumps, as well as fetch previous bumps of your server from specific channels. These are added to the bumps of each user, and can be displayed from a server-wide leaderboard.
## Polling
ZennDev can also conduct simple polling from yes or no to complex multiple choice polls. This uses reactions and will eventually support custom reactions.
## API Integration from Multiple Sources
Includes API integration from Discord for the bot, Steam for playercounts, and Replit for database storage.
# Command List
| Command       | Args.                                             | Description                                | Public? |
|---------------|---------------------------------------------------|--------------------------------------------|---------|
| help          | [type]                                            | Displays the help page                     | yes     |
| setup         | none                                              | Sets the server up for the first time      | no      |
| prefix        | <prefix>                                          | Changes the bot prefix                     | no      |
| codeadmin     | <role>                                            | Shows the disboard bump leaderboard        | no      |
| info          | [member]                                          | Shows data about the member                | yes     |
| invites       | [member]                                          | Returns the amount of invites a member has | yes     |
| leaves        | [member]                                          | Returns the amount of leaves a member has  | yes     |
| leaderboard   | [page]                                            | Displays the invite leaderboard            | yes     |
| iroles        | none                                              | Shows all the invite rewards of the server | yes     |
| addirole      | <invites> \<role>                                 | Adds a role reward                         | no      |
| delirole      | <invites> \<role>                                 | Deletes the specified role reward          | no      |
| fetch         | <invites\|bumps>                                  | Fetchs previous server stats.              | no      |
| edit          | <invites\|leaves\|bumps> <amount> [member]        | Sets the value of a member's stat          | no      |
| reactions     | none                                              | Shows all role reaction messages           | yes     |
| rr            | <channel> <message> <:reaction:> <role>           | Adds a role reaction to a message          | no      |
| delrr         | <channel> <message> <:reaction:> <role>           | Deletes a role reaction                    | no      |
| addcounter    | <tracker>                                         | Adds a Server Stats channel                | no      |
| delcounter    | <tracker>                                         | Removes a Server Stats channel             | no      |
| d leaderboard | [page]                                            | Shows the disboard bump leaderboard        | yes     |
| cross         | none                                              | Displays member not in the second server   | no      |
| poll          | <"desc"> ["opt1"]...                              | Creates a poll and deletes the message     | yes     |
| report        | none                                              | Creates a new report and DM's user for info| yes     |
| reportchannel | <channel>                                         | Changes the channel reports are sent to    | no      |