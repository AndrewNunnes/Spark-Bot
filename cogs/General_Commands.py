import discord
from typing import Optional
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import platform
import datetime
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

from discord import Colour, Member
from discord import Embed
from discord import __version__ as discord_version
from discord.ext.commands import BucketType, cooldown, bot_has_permissions, guild_only, Cog
from discord.ext.commands import command
from psutil import Process, virtual_memory

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

class General(commands.Cog, name="📯 General Category"):

    """`{General Commands}`"""

    def __init__(self, bot):
        self.bot = bot
        
   # @commands.command(aliases=['allcommands'])
   # @commands.guild_only()
   # async def commands(self, ctx):
     # """
    #  List of all commands
     # """
    #  bruh = "\n ".join([c.name for c in self.bot.commands])
      
     # embed = discord.Embed(
     #   title="__List of Commands__", 
       # description=bruh, 
      #  color=discord.Color.darker_grey())
      
    #  await ctx.send(embed=embed)

    @commands.Cog.listener()
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

        e.timestamp = datetime.datetime.utcnow()

        e.set_footer(text=message.author.mention, icon_url=message.author.avatar_url)

        #Adding the fields
        for name, value in fields:
          e.add_field(
            name=name, 
            value=value
          )

        await channel.send(embed=e)

        #If the channel doesn't exist
        #It'll send it in a different channel
        if not channel:

          e = discord.Embed(
            color=0x420000)

          fields = ["<:booster:741407205575622696> __*New Booster {!}*__", f'{message.author.mention}']

          e.timestamp = datetime.datetime.utcnow()

          e.set_footer(text=message.author.mention, icon_url=message.author.avatar_url)

          
          #Adding the fields
          for name, value in fields:
            e.add_field(
              name=name, 
              value=value
            )

          await message.channel.send(embed=e)

    @commands.command(
      brief="{Connection Test to Discord}", 
      usage="ping")
    @commands.guild_only()
    @commands.cooldown(3, 15, type=BucketType.user)
    async def ping(self, ctx):
      
        embed = discord.Embed(title='Pong?', color=discord.Color.dark_blue())
        await ctx.send(embed=embed, delete_after=0.3)
              
        await asyncio.sleep(0.5)
              
        embed = discord.Embed(title='My Connection:', description=f'__**My ping is {round(self.bot.latency * 1000)}ms**__', color=discord.Color.dark_blue())
        await ctx.send(embed=embed)
        
    @commands.command(
      brief="{List of Boosters for the Server}", 
      usage="boosters")
    @commands.guild_only()
    async def boosters(self, ctx):

      #Saving the guild's boosters
      #As a variable
      booster_list = ctx.guild.premium_subscribers

      #Checking to see if there is no boosters
      if booster_list == []:
        boosters = "No Boosters"
      else:
        boosters = booster_list

      e = discord.Embed(
        title=f"<:booster:741407205575622696> __*List of Boosters for {{{ctx.guild.name}}}*__", 
        description=f"{boosters}", 
        color=0x420000)

      e.add_field(
        name=f"__*Total*__", 
        value=f'{len(booster_list)} Boosters'
      )
      e.timestamp = datetime.datetime.utcnow()

      await ctx.send(embed=e)

    @commands.command(
      brief='{Shows info about the Bot}', 
      usage='binfo'
    )
    @commands.bot_has_permissions(embed_links=True)
    async def binfo(self, ctx):

        #Defining the embed
        #And adding our github, bot's avatar, etc.
        stats = discord.Embed(title="<:github:741045521577279559> Spark ++'s Source Code",
                      url="https://github.com/AndrewNunnes/Spark-Bot",
                      timestamp=datetime.datetime.utcnow())
        stats.set_thumbnail(url=self.bot.user.avatar_url)
        stats.set_footer(text=f"Requested by {ctx.author}", icon_url='{}'.format(ctx.author.avatar_url))

        # Grabbing technical statistics of the bot
        proc = Process()
        with proc.oneshot():
            uptime = datetime.timedelta(seconds=time() - proc.create_time())
            mem_total = virtual_memory().total / (1024 ** 2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        uptime_hours, uptime_remainder = divmod(uptime.seconds, 3600)
        uptime_minutes, uptime_seconds = divmod(uptime_remainder, 60)
        frmt_uptime = '{:01} Hour(s), {:01} Minute(s), {:01} Second(s)'.format(int(uptime_hours), int(uptime_minutes),
                                                                               int(uptime_seconds))

        # Grabbing total number of channels across all guilds in which the bot is present in
        channels = map(lambda m: len(m.channels), self.bot.guilds)

        # Setting up fields
        fields = [
            ("__*Developer*__", "Andrew Nunnes#1148", False),

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

            ("__*Line Count*__", lineCount(), True),
            ("__*Uptime*__", frmt_uptime, False),
            ("__*Latency*__", f'{round(self.bot.latency * 1000)}ms', False), 
            ("__*Memory Usage*__", f"{mem_usage:,.2f} / {mem_total:,.2f} MiB ({mem_of_total:.2f}%)", False)]

        # Add fields to the embed
        for name, value, inline in fields:
            stats.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=stats)
      
      #Old botinfo command
      #@commands.command(
        #brief="{Info about the Bot}",
        #usage="binfo")
      #@commands.guild_only()
      #@commands.cooldown(1 , 30, type=BucketType.channel)
      #async def binfo(self, ctx):
          
          #pythonVersion = platform.python_version()
          #dpyVersion = discord.__version__
          #serverCount = len(self.bot.guilds)
          #e = discord.Embed(title='My Info', color=discord.Color.darker_grey())
          #e.add_field(name='Creator:', value="Andrew Nunnes#1148", inline=True)
          #e.add_field(name='Python Version:', value=f"I'm running version {pythonVersion} of Python", inline=False)
          #e.add_field(name='Discord.py Version:', value=f"I'm running discord.py Version {dpyVersion}", inline=False)
          #e.add_field(name='Server Count:', value=f"I'm in {serverCount} server(s)", inline=False)
          #e.add_field(name='Invite Link', value="[Here!](https://discord.com/oauth2/authorize?client_id=721397896704163965&scope=bot&permissions=2146958847)", inline=True)
          #e.add_field(name='Current Prefix', value=f'{ctx.prefix}', inline=True)
          #e.add_field(name='')

          
          #await ctx.send(embed=e)

    @commands.command(
      brief="{Info about the Server}", 
      usage="sinfo")
    @commands.guild_only()
    @commands.cooldown(1, 30, type=BucketType.channel)
    @commands.bot_has_permissions(embed_links=True)
    async def sinfo(self, ctx):

        # Getting permissions of the bot within the channel
        perms = ctx.guild.me.permissions_in(ctx.message.channel)

        #memberCount = len(set(self.bot.get_all_members()))
        humans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))

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
          title=f'Server Info', 
          color=0x420000)

        #Getting the date this guild
        #Was created
        e.set_footer(text=f'Created · {ctx.guild.created_at.strftime("%d/%m/%Y")}')

        e.set_author(name=f"Command requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")

        #Adding the fields
        for name, value, inline in fields:
          e.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=e)

    @commands.command(
      brief="{Info on a User}", 
      usage="uinfo (member)")
    @commands.guild_only()
    @commands.cooldown(3, 20, type=BucketType.user)
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
            inline=inline
          )

        e.set_thumbnail(url=member.avatar_url)

        e.set_footer(text=f'{member.name}', icon_url=member.avatar_url)

        e.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=e)
          
    @commands.command(
      brief="{User's Avatar}", 
      usage="avatar (member)")
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(3, 20, type=BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):

        #Checks if a member is mentioned or not
        member = ctx.author if not member else member

        #Redefining member as userinfo 
        #Just to make it easier to read
        userinfo = member

        embed = discord.Embed(
          title=f"{userinfo.name}'s Avatar", 
          color=0x420000, 
          timestamp = datetime.datetime.utcnow())

        embed.set_author(name=f"Command requested by: {ctx.message.author}")

        #Getting the member's avatar url
        #And formatting as png
        embed.set_image(url=userinfo.avatar_url_as(format='png'))

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
