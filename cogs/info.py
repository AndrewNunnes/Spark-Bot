#•----------Modules----------•#

import discord

from typing import Optional, Union

import platform

from datetime import datetime

import random

import asyncio

import os

import pathlib

import random

import string

from asyncio.subprocess import Process

from platform import python_version

from time import time

from typing import Optional

from discord import __version__ as discord_version

from discord.ext.commands import command, BucketType, cooldown, bot_has_permissions, guild_only, Cog, has_permissions, BadUnionArgument

#from psutil import Process, virtual_memory

#•----------Variables---------•#
#Dict to go through when getting the guild region
region = {
  "eu-central": ":flag_eu: Central Europe", 
  "europe": ":flag_eu: Central Europe", 
  "singapore": ":flag_sg: Singapore", 
  "india": ":flag_in: India", 
  "japan": ":flag_jp: Japan", 
  "us-central": ":flag_us: Central US", 
  "sydney": ":flag_au: Sydney", 
  "us-east": ":flag_us: Eastern US", 
  "us-west": ":flag_us: Western US", 
  "us-south": ":flag_us: Southern US", 
  "eu-west": ":flag_eu: Western Europe", 
  "london": ":flag_gb: London", 
  "amsterdam": ":flag_nl: Amsterdam", 
  "hongkong": ":flag_hk: Hong Kong", 
  "russia": ":flag_ru: Russia", 
  "southafrica": ":flag_za: Southern Africa", 
  "brazil": ":flag_br: Brazil"
}

#•----------Functions----------•#

#Used to give a nicer looking region string
def get_region(disc_region, region_dict):
    
    for key in region_dict:
        if key == disc_region:
            return region_dict[key]
        else:
            pass
    
#Used to show the line count/file count of this bot
def lineCount():

    code = 0
    comments = 0
    blank = 0
    file_amount = 0
    ENV = "venv"

    for path, _, files in os.walk("."):
        for name in files:
            file_dir = str(pathlib.PurePath(path, name))
            # Ignoring the venv directory
            if not name.endswith(".py") or ENV in file_dir:
                continue
            file_amount += 1
            with open(file_dir, "r", encoding="utf-8") as file:
                for line in file:
                    if line.strip().startswith("#"):
                        comments += 1
                    elif not line.strip():
                        blank += 1
                    else:
                        code += 1

    # Adding up the total lines of code
    total = comments + blank + code

    return "Code: {}\n" \
           "Commentary: {}\n" \
           "Blank: {}\n" \
           "Total: {}\n" \
           "Files: {}".format(code, comments, blank, total, file_amount)
           
#•----------Class----------•#

class Info(Cog, name="Info Category"):

    """`{Info Commands}`"""

    def __init__(self, bot):
        self.bot = bot
        
#•----------Events----------•#

    @Cog.listener()
    async def on_message(self, message):

        if message.type == discord.MessageType.premium_guild_subscription:

          guild = message.guild

          names = ['boost', 'announce']

          #Check for a boost/announce channel
          #And send it there
          channel = discord.utils.find(
            lambda channel:any(
              map(lambda c: c in channel.name, names)), 
              guild.text_channels) 

          e = discord.Embed(
            color=0x420000)

          fields = ["<:booster:741407205575622696> __*New Booster {!}*__", f'{message.author.mention}']

          e.timestamp = datetime.utcnow()

          e.set_footer(text=message.author.mention, icon_url=message.author.avatar_url)

          #Adding the fields
          for name, value in fields:
            e.add_field(
              name=name, 
              value=value)

          await channel.send(embed=e)

          #If the channel doesn't exist
          #It'll send it in a different channel
          if not channel:

            e = discord.Embed(
              color=0x420000)

            fields = ["<:booster:741407205575622696> __*New Booster {!}*__", f'{message.author.mention}']

            e.timestamp = datetime.utcnow()

            e.set_footer(text=message.author.mention, icon_url=message.author.avatar_url)
          
            #Adding the fields
            for name, value in fields:
              e.add_field(
                name=name, 
                value=value
              )

            await message.channel.send(embed=e)
            
#•----------Commands----------•#

    @command(
        brief='{Shows info about the Bot}', 
        usage='binfo', 
        aliases=['botinfo', 'sparkinfo', 'about'])
    @cooldown(1, 1.5, BucketType.user)
    @guild_only()
    @bot_has_permissions(use_external_emojis=True, embed_links=True)
    async def binfo(self, ctx):

        #Defining the embed
        #And adding our github, bot's avatar, etc.
        stats = discord.Embed(
            title="<:github:741045521577279559> Spark ++'s Source Code",
            
            url="https://github.com/AndrewNunnes/Spark-Bot")
            
        stats.set_thumbnail(url=self.bot.user.avatar_url)

        # Grabbing technical statistics of the bot
        #proc = Process()
        #with proc.oneshot():
            #uptime = datetime.timedelta(seconds=time() - proc.create_time())
            #mem_total = virtual_memory().total / (1024 ** 2)
            #mem_of_total = proc.memory_percent()
            #mem_usage = mem_total * (mem_of_total / 100)

        #uptime_hours, uptime_remainder = divmod(uptime.seconds, 3600)
        #uptime_minutes, uptime_seconds = divmod(uptime_remainder, 60)
        #frmt_uptime = '{:01} Hour(s), {:01} Minute(s), {:01} Second(s)'.format(int(uptime_hours), int(uptime_minutes),
                                                                               #int(uptime_seconds))

        # Grabbing total number of channels across all guilds in which the bot is present in
        channels = map(lambda m: len(m.channels), self.bot.guilds)
        
        #Used to display my name
        owner = ctx.guild.get_member(265313384033943553)

        # Setting up fields
        fields = [
            ("__*Developer*__", owner.mention, False),

            ("__*Language | Library*__",
             f"<:Python_Logo:741046229441708152> Python {python_version()} | <:discord:741045246435262482> Discord.py {discord_version}",
             False),

            ("__*<:discord:741045246435262482> Support Server*__",
             "[Here!](https://discord.com/invite/fkdW9hB)", True),

            ("__*<:invite:741045282929901678> Invite Link*__",
             "[Here!](https://discord.com/oauth2/authorize?client_id=721397896704163965&scope=bot&permissions=470117623)", True),

            ("__*❗ Current Prefix*__", f'`{ctx.prefix}`', True),

            ("__*Discord Stats*__",
             "All Guilds: {}"
             "\nAll Channels: {}"
             "\nAll Emojis: {}"
             "\nAll Commands: {}"
             "\nAll Users: {:,}".format(len(self.bot.guilds), sum(list(channels)), len(self.bot.emojis),
                                    len(self.bot.commands),
                                    len(self.bot.users)), True),

            #("__*Line Count*__", lineCount(), True),
            #("__*Uptime*__", frmt_uptime, False),
            ("__*Latency*__", f'{round(self.bot.latency * 1000)}ms', False)]#
            #("__*Memory Usage*__", f"{mem_usage:,.2f} / {mem_total:,.2f} MiB ({mem_of_total:.2f}%)", False)]

        # Add fields to the embed
        for name, value, inline in fields:
            stats.add_field(name=name, value=value, inline=inline)
            
        stats.set_footer(
            text=f"Bot Created At | {self.bot.user.created_at.strftime('%a/%b %d/%Y • %I:%M %p')}")
 
        await ctx.send(embed=stats)

    @command(
        brief="{Info about the Server}", 
        usage="sinfo", 
        aliases=['si', 'serverinfo'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def sinfo(self, ctx):
         
        g = ctx.guild

        # Getting permissions of the bot within the channel
        perms = ctx.guild.me.permissions_in(ctx.message.channel)

        #memberCount = len(set(self.bot.get_all_members()))
        humans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
        
        #Check if there's more than 20 emojis
        if len(g.emojis) > 20:
            length = len(g.emojis) - 20
            
            emojis = f"{' '.join(map(str, g.emojis[:20]))} and **{length}** more..."
        #If there's less than 20 emojis
        else:
            emojis = " ".join(map(str, g.emojis))
            
        emojis = "No Emojis" if emojis == "" else emojis

        #Get statuses
        statuses = [len(list(filter(lambda m: str(m.status) == "online" , g.members))),
                    len(list(filter(lambda m: str(m.status) == "idle" , g.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd" , g.members))),
                    len(list(filter(lambda m: str(m.status) == "offline" , g.members)))]

        #Getting the # of bans
        #In the server
        bans = len(await g.bans()) if perms.ban_members else "N/A"

        #Getting the # of invites
        #In the server
        invites = len(await g.invites()) if perms.manage_guild else "N/A"

        #List of fields to add to the embed
        fields = [
                  ("__*Owner*__", g.owner.mention, False), 
                  
                  (f"__*Members*__ **{{{len(g.members)}}}**", 
                  f'Statuses: <:online:728377717090680864>{statuses[0]}, <:idle:728377738599071755>{statuses[1]}, <:dnd:728377763458973706>{statuses[2]}, <:offline:728377784207933550>{statuses[3]}' +
                  f"\nBanned: {bans}" +
                  f"\nHumans: {humans}" +
                  f"\nBots: {bots}", True), 
                  
                  ("__*Misc*__", 
                  f"{get_region(str(g.region), region)}" +
                  f'\n<:textch:728377808518381679> {len(ctx.guild.text_channels)} Text Channels' +
                  f'\n<:voicech:728377834187259976> {len(ctx.guild.voice_channels)} Voice Channels' +
                  f'\n🔗 {invites} Invites', True),
                  
                  (f"__*Emojis*__ **{{{len(g.emojis)}}}**", 
                  emojis, True)]
                  
        e = discord.Embed(
            title=f'__*{{General Info for {ctx.guild}}}*__')
        
        #Getting the date this guild
        #Was created
        e.set_footer(
            text=f'Created On | {ctx.guild.created_at.strftime("%a/%b %d/%Y • %I:%M %p")}')

        e.set_thumbnail(
            url=ctx.guild.icon_url)

        #Adding the fields
        for name, value, inline in fields:
            e.add_field(
                name=name, 
                value=value, 
                inline=inline)

        await ctx.send(embed=e)

    @command(
        brief="{Info on a User}", 
        usage="uinfo (member)", 
        aliases=['ui', 'userinfo'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def uinfo(self, ctx, member: discord.Member = None):

        #Checks if a member is mentioned 
        #Or if it's the author
        member = ctx.author if not member else member

        # Check if user roles is greater than 20
        if len(member.roles) > 12:
            # Retrieve the length of the remaining roles
            length = len(member.roles) - 12

            # Store the first 12 roles in a string called "roles" (highest to lowest)
            role = f"{' '.join(map(str, (role.mention for role in list(reversed(member.roles))[:12])))} and **{length}** more"

        else:
            # Display all roles as it is lower than 12
            role = f"{' '.join(map(str, (role.mention for role in list(reversed(member.roles[1:])))))}"

        # Accounting for the edge case where the user has no roles to be displayed
        roles = "No Roles" if role == "" else role
        
        nick = "No Nick" if not member.nick else member.nick

        fields = [
                  (f"__*Roles*__ **{{{len(member.roles[1:])}}}**", 
                  f"Roles -> {roles}" +
                  f"\nTop Role -> {member.top_role.mention}", False), 
                  
                  ("__*Account*__", 
                  f"Status -> {str(member.status).title()}" +
                  f"\nCreated On | {member.created_at.strftime('%a/%b %d/%Y • %I:%M %p')}" +
                  f"\nJoined On | {member.joined_at.strftime('%a/%b %d/%Y • %I:%M %p')}", True),
                  
                  ("__*Misc*__", 
                  f"Nick -> {nick}" +
                  f"\nBoosting? -> {bool(member.premium_since)}" +
                  f"\nBot? -> {member.bot}", False)]
                  
        e = discord.Embed(
            description=f"*{{General Info for {member}}}*")
            
        #Adding the fields
        #To the embed
        for name, value, inline in fields:
            e.add_field(
                name=name, 
                value=value, 
                inline=inline)

        e.set_thumbnail(
            url=member.avatar_url)

        e.set_footer(
            text=f"ID -> {member.id}")

        e.timestamp = datetime.utcnow()

        await ctx.send(embed=e)

    @command(
        name="roleinfo", 
        brief="{Get Info on a Role}", 
        usage="roleinfo <role>", 
        aliases=['ri', 'rinfo'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def info(self, ctx, *, role: discord.Role):
          
        #See when the role was created
        role_created = f"{role.created_at.strftime('%a/%b %d/%Y • %I:%M %p')}"
        
        #List number of non-bots
        humans = len(list(filter(lambda h: not h.bot, role.members)))
        
        #List number of bots
        bots = len(list(filter(lambda b: b.bot, role.members)))
        
        #If there is more than 15 members
        if len(role.members) > 25:
            length = len(role.members) - 25
        
            human_list = f"{' , '.join(map(str, (member.mention for member in list(reversed(role.members))[:25])))} and **{length}** more"
        #If there is less than 25 members
        else:
            human_list = f"{' , '.join(map(str, (member.mention for member in (list(reversed(role.members))))))}"
        
        #If there is no members 
        human_lt = "No Members" if human_list == "" else human_list
        
        #Custom emojis
        check = "<:greenmark:738415677827973152>"
        x = "<:redmark:738415723172462723>"
        
        #Using emojis from above
        #To show any bools
        mentionable = check if role.mention else x
        hoisted = check if role.hoist else x
        
        e = discord.Embed(
            description=f"**General Info for {role.mention} {{Color In Hex > {role.color}}}**")
      
        #Make fields
        fields = [("ID", role.id, True),
        
                  ("Misc", 
                  f"\nMentionable? {mentionable}" +
                  f"\nDisplays from Others? {hoisted}", True), 
      
                  ("Position", role.position, True), 
                
                  (f"Members w/{role.name} {{{len(role.members)}}}", 
                  f"\nHumans: {humans}" +
                  f"\nBots: {bots}", False), 
                  
                  (f"List of Members with this Role", human_lt, False)]
                  
        #Show when role was created
        e.set_footer(
            text=f"Role Created At | {role_created}")
            
        e.set_author(
            name=f"Requested by {ctx.author}", 
            icon_url=ctx.author.avatar_url)
        
        #Add fields     
        for name, val, inl in fields:
            e.add_field(
                name=name, 
                value=val, 
                inline=inl)
      
        await ctx.send(embed=e)

    @command(
        name="rolelist", 
        brief="{List all Roles in Server/Member}", 
        usage="rolelist (member)", 
        aliases=['rlist', 'rlst'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def _list(self, ctx, item: Optional[discord.Member]):
      
        guild = ctx.guild
        
        #If a member is mentioned
        if isinstance(item, discord.Member):
            rolelist = item.roles
            #Used to show in the embed's description
            #'[1:]' removes the @@everyone role
            #From being counted
            role_count = f"*Roles for {item.display_name} | Total* **{{{len(rolelist[1:])}}}**"
            #Used to show the embed's thumbnail
            #As the member's avatar
            thumbnail = item.avatar_url
        
        else:
            #Variable for getting roles in guild
            rolelist = guild.roles
            #Used to show in the embed's description
            #'[1:]' removes the @@everyone role
            #From being counted
            role_count = f"*Roles for {ctx.guild} | Total* **{{{len(rolelist[1:])}}}**"
            #Used to show the embed's thumbnail
            #As the guilds icon
            thumbnail = ctx.guild.icon_url
    
        #Check if there is 
        #Over 25 roles in the guild
        if len(rolelist) > 25:
            #Get the length of remaining roles
            length = len(rolelist) - 25
        
            role = f"{' • '.join(map(str, (role.mention for role in list(reversed(rolelist))[:20])))} and **{length}** more"
        
        #If there is less than 25 roles
        #In the guild
        else:
            role = f"{' • '.join(map(str, (role.mention for role in list(reversed(rolelist[1:])))))}"
        
        #Check if there is no roles to display
        roles = "No Roles" if role == "" else role
    
        #Make and send embed
        e = discord.Embed(
            title=role_count, 
            description=roles, 
            timestamp=datetime.utcnow())
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        e.set_thumbnail(
            url=thumbnail)

        await ctx.send(embed=e)
          
    @command(
        brief="{Get a List of Perms for a Role/Member}", 
        usage="perms <role>/(member)", 
        aliases=['permission', 'permissions'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def perms(self, ctx, *, item: Optional[Union[discord.Role, discord.Member]]):
        
        greenmark = "<:greenmark:738415677827973152>" 
        redmark = "<:redmark:738415723172462723>"
        garbage = "<:trash:734043301187158082>"
        
        #Make optional to mention a member
        item = item if item else ctx.author
        
        if isinstance(item, discord.Member):
            #Iterating through list of guild perms
            perms = [f"{perm.title().replace('_', ' ')} = {greenmark if value else redmark}" for perm, value in item.guild_permissions]
            #Member's avatar for the embed thumbnail
            thumbnail = item.avatar_url

        else:
            #Iterating through list of general perms
            perms = [f"{perm.title().replace('_', ' ')} = {greenmark if value else redmark}" for perm, value, in item.permissions]
            #Guilds icon for the embed thumbnail
            thumbnail = ctx.guild.icon_url
        
        #Split the list of perms into 2
        middle = len(perms) // 2
        f_half = "\n".join(perms[:middle])
        s_half = "\n".join(perms[middle:])
        
        #List of contents go through
        #Inside of our embeds
        contents = [f_half, s_half]
        
        intro = f"__*Showing All Permissions for {item.mention}*__"
        
        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            description=f"{intro}\n\n{contents[cur_page-1]}", 
            timestamp=datetime.utcnow())
        e.set_thumbnail(
            url=thumbnail)

        e.set_author(
            name=f"Page {cur_page}/{pages}")
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        
        #Store the first embed we're sending
        msg = await ctx.send(embed=e)
        
        #Reactions to add
        emotes = ['⬅️', '➡️', '⏹']
        for react in emotes:
            #Add the reactions
            await msg.add_reaction(react)
        
        #Custom check to check for the author of the command
        #And check for the right emojis
        #And check for the specific message
        def checkauth(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await msg.edit(embed=err)
                await msg.clear_reactions()
                break
              
            else:
                #Check for the specific emoji
                #And if the user isn't trying to go to the negative side 
                #Of pages
                if str(reaction.emoji) == '⬅️' and cur_page > 1:
                    await msg.remove_reaction(reaction, user)
                    cur_page -= 1
                    
                    e = discord.Embed(
                        description=f"{intro}\n\n{contents[cur_page-1]}", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=thumbnail)
                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                #Check for the specific emoji
                #And if the user tries to go forward too much
                elif str(reaction.emoji) == '➡️' and cur_page != pages:
                    await msg.remove_reaction(reaction, user)
                    cur_page += 1
                    
                    e = discord.Embed(
                        description=f"{intro}\n\n{contents[cur_page-1]}", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=thumbnail)
                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                        
                    await msg.edit(embed=e)
                
                #Used to delete the embed
                elif str(reaction.emoji) == '⏹':
                    await msg.clear_reactions()
                    e = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    await msg.edit(embed=e, delete_after=5)
                
                else:
                    await msg.remove_reaction(reaction, user)

    @command(
        brief="{Info on a Channel}", 
        usage="chinfo <#channel>", 
        aliases=['channelinfo'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def chinfo(self, ctx, channel: Optional[Union[discord.TextChannel, discord.VoiceChannel]]=None):
        
        channel = ctx.channel if not channel else channel
        
        #If there is more than 15 Members in VC
        if len(channel.members) > 15:
            length = len(channel.members) - 15
         
            member_list = f"{' , '.join(map(str, (member.mention for member in list(reversed(channel.members))[:15])))} and **{length}** more"
    
        #If there is less than 15 members in VC
        else:
            member_list = f"{' , '.join(map(str, (member.mention for member in list(reversed(channel.members)))))}"
    
        #Check there is no members
        mem_list = "No Members" if member_list == "" else member_list
    
        #When the channel was created
        created_at = channel.created_at.strftime('%a/%b %d/%Y • %I:%M %p')
    
        #If user says a voice channel
        if isinstance(channel, discord.VoiceChannel):

            e = discord.Embed(
                description=f"**General Info for {channel.mention}**")
      
            #Embed fields
            fields = [("__*ID*__", channel.id, False),
      
                    ("__*Position*__", channel.position, False), 
                
                    ("__*Misc*__", 
                    f"\nBit Rate: {channel.bitrate}" +
                    f"\nUser Limit {channel.user_limit}", True), 
                
                    (f"__*Members currently in VC {{{len(channel.members)}}}*__", 
                    f"\nHumans: {len(list(filter(lambda h: not h.bot, channel.members)))}" +
                    f"\nBots: {len(list(filter(lambda b: b.bot, channel.members)))}", False), 
                
                    ("__*List of Members currently in VC*__", 
                    f"\n{mem_list}", False)]
                
            #Add fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
      
            #Set footer and show when channel was created
            e.set_footer(
                text=f"Channel Created | At {created_at}")
      
            #Show who requested the command
            e.set_author(
                name=f"Requested by {ctx.author}", 
                icon_url=ctx.author.avatar_url)
    
        #If user mentions a text channel
        elif isinstance(channel, discord.TextChannel):
      
            channel = ctx.channel if not channel else channel
      
            #Define the channel's topic
            topic = channel.topic
      
            #If there isn't a topic
            if topic is None:
                topic = "No Topic"
            #If there is a topic
            else:
                topic = topic
      
            #Define the category channel's under
            under_categ = channel.category
      
            #If it isn't under a category
            if under_categ is None:
                under_categ = "No Category"
            #Else if it is under a category
            else:
                under_categ = under_categ

            #Make embed
            e = discord.Embed(
                description=f"**General Info for {channel.mention}**")

            #Make fields
            fields = [("__*ID*__", channel.id, False), 
      
                    ("__*Position*__", channel.position, False), 
                
                    ("__*Channel Topic*__", topic, True), 
                
                    ("__*Misc*__", 
                    f"\nSlowmode Delay: {channel.slowmode_delay}" +
                    f"\nNSFW? {channel.is_nsfw()}" +
                    f"\nNews Channel? {channel.is_news()}", True), 
                
                    ("__*Category it's Under*__", under_categ, True)]
                
            #Add fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
      
            #Show when the channel was created
            e.set_footer(
                text=f"Channel Created At | {created_at}")
      
            #Show who requested the command
            e.set_author(
                name=f"Requested by {ctx.author}", 
                icon_url=ctx.author.avatar_url)
        
        #If they mention a non-existing channel
        else:
      
            e = discord.Embed(
                description="⚠️ **That Channel doesn't exist**", 
                color=0x420000)
        
        await ctx.send(embed=e)

    @chinfo.error
    async def chinfo_error(self, ctx, error):
        if isinstance(error, BadUnionArgument):
            e = discord.Embed(
                description='Either:\n• When specifying a Voice Channel, only use the name of it\nExample: `!chinfo "Voice Channel"`\n• That Channel does not exist', 
                color=0x420000)
        
            await ctx.send(embed=e)
          
    @command(
        brief="{User's Avatar}", 
        usage="avatar (member)", 
        aliases=['av', 'ava', 'pfp'])
    @guild_only()
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1.5, BucketType.user)
    async def avatar(self, ctx, member: Optional[discord.Member] = None):

        #Checks if a member is mentioned or not
        member = ctx.author if not member else member

        e = discord.Embed(
          title=f"{member}'s Avatar", 
          url=str(member.avatar_url), 
          timestamp = datetime.utcnow())

        e.set_footer(
            text=f"Requested by {ctx.message.author}")

        e.set_image(
            url=str(member.avatar_url))

        await ctx.send(embed=e)

#•----------Setup/Add this Cog----------•#

def setup(bot):
    bot.add_cog(Info(bot))
