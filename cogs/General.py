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

from discord.ext.commands import command, BucketType, cooldown, bot_has_permissions, guild_only, Cog, has_permissions

#from psutil import Process, virtual_memory

#•----------Functions----------•#

def lineCount():
    """Getting the line count of the project"""

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
      usage='binfo'
    )
    @cooldown(1, 1.5, type=BucketType.user)
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
      usage="sinfo")
    @guild_only()
    @cooldown(1, 1.5, type=BucketType.user)
    @bot_has_permissions(embed_links=True)
    async def sinfo(self, ctx):

        # Getting permissions of the bot within the channel
        perms = ctx.guild.me.permissions_in(ctx.message.channel)

        #memberCount = len(set(self.bot.get_all_members()))
        humans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))

        #Get statuses
        statuses = [len(list(filter(lambda m: str(m.status) == "online" , ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle" , ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd" , ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline" , ctx.guild.members)))]

        #Getting the # of bans
        #In the server
        bans = len(await ctx.guild.bans()) if perms.ban_members else "N/A"

        #Getting the # of invites
        #In the server
        invites = len(await ctx.guild.invites()) if perms.manage_guild else "N/A"

        #List of fields to add to the embed
        fields = [("__*Name*__", ctx.guild.name, True), 

                  ("__*Region*__", ctx.guild.region, True), 

                  ("__*Owner*__", ctx.guild.owner, True), 

                  ("__*Members*__", 
                  f"Total: {len(list(ctx.guild.members))}"
                  f'\nStatuses: <:online:728377717090680864>{statuses[0]}, <:idle:728377738599071755>{statuses[1]}, <:dnd:728377763458973706>{statuses[2]}, <:offline:728377784207933550>{statuses[3]}'
                  f"\nBanned: {bans}"
                  f"\nHumans: {humans}"
                  f"\nBots: {bots}", True), 

                  ("__*Channels*__", f'<:textch:728377808518381679>{len(ctx.guild.text_channels)}\n<:voicech:728377834187259976>{len(ctx.guild.voice_channels)}', True), 
                  
                  ("__*# of Invites*__", invites, True)]

        e = discord.Embed(
            title=f'General Info for {ctx.guild}', 
            color=0x420000)

        #Getting the date this guild
        #Was created
        e.set_footer(
            text=f'Created · {ctx.guild.created_at.strftime("%d/%m/%Y, %I:%H:%M")}')

        e.set_author(
            name=f"Command requested by: {ctx.author}", 
            icon_url=f"{ctx.author.avatar_url}")
            
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
    @cooldown(1, 1.5, type=BucketType.user)
    async def uinfo(self, ctx, member: discord.Member = None):

        #Checks if a member is mentioned 
        #Or if it's the author
        member = ctx.author if not member else member

        # Check if user roles is greater than 20
        if len(member.roles) > 20:
            # Retrieve the length of the remaining roles
            length = len(member.roles) - 20

            # Store the first 20 roles in a string called "roles" (highest to lowest)
            role = f"{' '.join(map(str, (role.mention for role in list(reversed(member.roles))[:20])))} and **{length}** more"

        #rolelist = [role.mention for role in member.roles[1:2047]]
        else:
            # Display all roles as it is lower than 20
            role = f"{' '.join(map(str, (role.mention for role in list(reversed(member.roles[1:])))))}"

        # Accounting for the edge case where the user has no roles to be displayed
        roles = "No Roles" if role == "" else role

        fields = [("__*Discord Tag*__", member.name, True), 

                  ("__*Nick*__", member.nick, True), 

                  ("__*ID*__", member.id, True), 

                  ("__*Created*__", member.created_at.strftime('%a %#d %B %Y, %I:%M %p'), True), 

                  ("__*Joined*__", member.joined_at.strftime('%a %#d %B %Y, %I:%M %p'), True), 

                  ("__*Roles*__", roles, False), 

                  ("__*Top Role*__", member.top_role.mention, False), 

                  ("__*Status*__", str(member.status).title(), True),

                  ("__*Boosting Server*__", bool(member.premium_since), True),

                  ("__*Bot?*__", member.bot, True)]

        e = discord.Embed(
            title=f"{{{member.name}'s General Info}}", 
            color=0x420000)

        #Adding the fields
        #To the embed
        for name, value, inline in fields:
            e.add_field(
                name=name, 
                value=value, 
                inline=inline)

        e.set_thumbnail(url=member.avatar_url)

        e.set_footer(
            text=f'{member.name}', 
            icon_url=member.avatar_url)

        e.timestamp = datetime.utcnow()

        await ctx.send(embed=e)

    @command(
      name="roleinfo", 
      brief="{Get Info on a Role}", 
      usage="roleinfo <role>", 
      aliases=['ri', 'rinfo'])
    @guild_only()
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
            human_list = f"{' , '.join(map(str, (member.mention for member in (list(reversed(role.members[1:]))))))}"
        
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
        brief="{Info on a Channel}", 
        usage="chinfo <#channel>", 
        aliases=['channelinfo'])
    @guild_only()
    async def chinfo(self, ctx, channel: Union[discord.TextChannel, discord.VoiceChannel]):
    
        #If there is more than 15 Members in VC
        if len(channel.members) > 15:
            length = len(channel.members) - 15
         
            member_list = f"{' , '.join(map(str, (member.mention for member in list(reversed(channel.members))[:15])))} and **{length}** more"
    
        #If there is less than 15 members in VC
        else:
            member_list = f"{' , '.join(map(str, (member.mention for member in list(reversed(channel.members[1:])))))}"
    
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
      
            channel = ctx.channel if channel else channel
      
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
      usage="avatar (member)")
    @guild_only()
    #@bot_has_permissions(embed_links=True)
    @cooldown(1, 1.5, type=BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):

        #Checks if a member is mentioned or not
        member = ctx.author if not member else member

        #Redefining member as userinfo 
        #Just to make it easier to read
        userinfo = member

        embed = discord.Embed(
          title=f"{userinfo.name}'s Avatar", 
          color=0x420000, 
          timestamp = datetime.utcnow())

        embed.set_author(name=f"Command requested by: {ctx.message.author}")

        #Getting the member's avatar url
        #And formatting as png
        embed.set_image(url=userinfo.avatar_url_as(format='png'))

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
