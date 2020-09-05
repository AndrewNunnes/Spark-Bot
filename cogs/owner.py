
#•----------Modules----------•#
import discord

from discord.ext.commands import command, Cog, BucketType, is_owner, guild_only, \
Converter, Greedy, cooldown, has_permissions, bot_has_permissions

from datetime import datetime

import asyncio

from typing import Optional

from aiohttp import ClientSession

from random import randint

import traceback

import os

import re

time_regex = re.compile("(?:(\d{1,5})(d|days|day|hours|hrs|hour|hr|h|m|minutes|minute|min|mins|seconds|second|sec|secs|s))+?")
#Our dictionary of possible responses
#For when the user gives a time in a command
time_dict = {
  "h": 3600, 
  
  "hours": 3600, 
  
  "hour": 3600, 
  
  "hr": 3600, 
  
  "hrs": 3600, 
  
  "m": 60, 
  
  'minutes': 60, 
  
  'minute': 60, 
  
  'mins': 60, 
  
  "min": 60, 
  
  "days": 86400, 
  
  "day": 86400, 
  
  "d": 86400, 
  
  "s": 1, 
  
  "seconds": 1, 
  
  "sec": 1, 
  
  "secs": 1,  
  
  "second": 1
}

#•----------Class(es)----------•#

#Used to convert the amount of time a user gives
class TimeConverter(Converter):
    async def convert(self, ctx, argument):
        args = argument.lower().split(" ")
        matches = re.findall(time_regex, "".join(args))
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise BadArgument(f"{value} is an invalid time key. Either give days, hours, minutes, or seconds")
            except ValueError:
                raise BadArgument(f"{key} isn't a number")
        return round(time)

class Owner(Cog, name="Owner Category"):
  
    """`{Commands for the One and Only Bot Owner}`"""
  
    def __init__(self, bot):
        self.bot = bot

        self.db = self.bot.get_cog('Database')
        
        self.ses = ClientSession(loop=self.bot.loop)
        
        #Set the role persist to False on default
        self.per = False
    
    def cog_unload(self):
        self.bot.loop.create_task(self.ses.close())
        
#•----------Commands----------•#
    
    @group(
        brief="{Menu for Role Persist}", 
        usage="rolepersist", 
        aliases=['rpersist'])
    @guild_only()
    @cooldown(1, 2.0, BucketType.user)
    @is_owner()
    async def rolepersist(self, ctx):
        
        e = discord.Embed(
            description="**Role Persist System**")
        #Make the fields
        fields = [
                  (f"• **status :** `{ctx.prefix}rolepersist status`", "{Show the Current Status for Role Persist}", False), 
        
                  (f"• **turn :** `{ctx.prefix}rolepersist turn <on/off>`", "{Turn On/Off Role Persist}", False)]
        
        #Add the fields
        for n, v, i in fields:
            e.add_field(
                name=n, 
                value=v, 
                inline=i)
        
        await ctx.send(embed=e)
    
    @rolepersist.command(
        brief="{Show the Current Status for Role Persist}", 
        usage="rolepersist status")
    @guild_only()
    @cooldown(1, 2.0, BucketType.user)
    @is_owner()
    async def status(self, ctx):
        
        #Used to check if role persist is on
        rpersist = bool(self.per)
        
        rpers = "on" if rpersist else "off"
        
        #Used to show an emoji if role persist
        #Is on/off
        state = "<:online:728377717090680864>" if rpersist else "<:offline:728377784207933550>"
        
        e = discord.Embed(
            description=f"{state} **Role Persist is currently {rpers}**", 
            color=0x420000)
        
        await ctx.send(embed=e)
        
    @rolepersist.command(
        brief="{Turn On/Off Role Persist}", 
        usage="rolepersist turn <on/off>", 
        aliases=['change'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    @is_owner()
    async def turn(self, ctx, state: bool):
        
        #If the user says on
        if state is True:
            #Set our local variable to true
            self.per = True
            await ctx.send("<:online:728377717090680684> Role Persist has been turned on")
        
        else:
            self.per = False
            
            await ctx.send("<:offline:7283777842079933550> Role Persist has been turned off")

    @command(
        brief="{Temporarily Ban a User}", 
        usage="tempban <user> (reason) <time>", 
        aliases=['temporaryban'])
    @guild_only()
    #@bot_has_permissions(ban_members=True)
    #@has_permissions(ban_members=True)
    #@cooldown(1, 5, BucketType.user)
    @is_owner()
    async def tempban(self, ctx, member: discord.Member, *, time: TimeConverter):
        
        redmark = "<:redmark:738415723172462723>"
        
        #If a time isn't given
        if not time:
            e = discord.Embed(
                description=f"{redmark} __*{ctx.author.mention}, you have to give a time for this user to be banned for*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return

        try: 
            #Make the embed
            e = discord.Embed(
                timestamp=datetime.utcnow(), 
                description=f"⚠️ **Temp Ban**", 
                color=0x420000)
            
            e.set_thumbnail(
                url=ctx.guild.icon_url)
            
            e.set_footer(
                text=f"Banned from {ctx.guild}")
            
            #Make fields
            fields = [
                     ("__*Time Banned for*__", time, False), 
                     
                     ("__*Temp Banned By*__", ctx.author.mention, False)]
            
            #Add the fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
            await member.send(embed=e)
        
        except Exception:
            pass
        
        #Ban the member
        await ctx.guild.ban(
            user=member)

        e = discord.Embed(
            timestamp=datetime.utcnow(), 
            description=f"<:ban:741030012848832533> **{member.mention} was temp banned!**", 
            color=0x420000)
        
        e.set_author(
            name=f"Duration -> {time}")
        
        e.set_footer(
            text=f"ID -> {member.id}")
        
        await ctx.send(embed=e)
        
        #Wait for the amount of time to unban the user
        await asyncio.sleep(time)
        
        #Unban the user
        await ctx.guild.unban(user=member)
        
        try:
            await member.send("Unbanned")
        except Exception:
            pass
        
        await ctx.send(f"{member.mention} has successfully been unbanned after {time}")
        
    @command()
    @is_owner()
    async def upcoming(self, ctx):
        
        url = "https://api.themoviedb.org/3/movie/upcoming?api_key= Your_api_key"
        r = await self.ses.get(url)
        
        respon = await r.json()
        
        resp = respon['results']
        
        page = 0
        
        msg = None
        
        #Check for making sure only author
        #Can trigger reactions
        def author(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']
            
        while True:
            #Text for each page
            body = '' 
            #Iterate through the dict/json
            #for n in resp[page]:
                #Add to the empty string

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=author)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                await ctx.send(embed=e)
                break
            
            else:
                if str(reaction.emoji) == '⬅️':
                    await m.remove_reaction(reaction, user)
                    page -= 1
                    
                elif str(reaction.emoji) == '➡️':
                    await m.remove_reaction(reaction, user)
                    page += 1
                    
                else:
                    await m.remove_reaction(reaction, user)

    @command(
        brief="{List of Upcoming Movies}", 
        usage="upcmovie", 
        aliases=['upcomingmovies', 'moviesupcoming', 'movieupc'])
    @guild_only()
    #@cooldown(1, 2.5, BucketType.user)
    #@bot_has_permissions(use_external_emojis=True)
    @is_owner()
    async def upcmovie(self, ctx):
        
        url = "https://api.themoviedb.org/3/movie/upcoming?api_key= Your_api_key"
        #Get the url with aiohttp session
        r = await self.ses.get(url)
        
        #Convert into json format to make easier
        #To access
        respon = await r.json()
        
        #Define the json response to make stuff easier
        #To access
        res = respon['results']
            
        page = 0
        
        def author(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']
        
        while True:
            
            try:
                #Wait for the user's reaction
                reaction, user = await self.bot.wait_for('reaction_add', check=author, timeout=180.0)
            
            #If user takes too long
            except asyncio.TimeoutError:
                await ctx.send("Took too long")
                break
            
            else:
                #Edit embed with previous page
                if str(reaction.emoji) == '⬅️':
                    await m.remove_reaction(reaction, user)
                    
                    page -= 1
                
                #Edit embed with next page
                elif str(reaction.emoji) == '➡️':
                    await m.remove_reaction(reaction, user)
                    
                    page += 1
                
                #If user tries to go to far back/forward
                else:
                    await m.remove_reaction(reaction, user)
            
    @command(
        brief="{List of Popular TV Shows}", 
        usage="populartv (page)", 
        aliases=['tvpopular', 'popularshows'])
    @guild_only()
    #@cooldown(1, 2.5, BucketType.user)
    #@bot_has_permissions(use_external_emojis=True)
    @is_owner()
    async def populartv(self, ctx, page_num: Optional[int]):
        
        redmark = "<:redmark:738415>"
        
        #Api key needed to have this work
        #Check their website to make one
        url = f"https://api.themoviedb.org/3/tv/popular?api_key=Your_api_key"
        r = await self.ses.get(url)

        #Convert into a json format
        #To make stuff easier to access
        resp = await r.json()
        #Used to show pages
        p = resp['page']
        totalp = resp['total_pages']
        totalr = resp['total_results']
        
        if page_num is not None:
            #Used to show the current page/total pages
            m = resp['results'][page_num]
        else:
            m = resp['results'][0]
        
        #If something with api goes wrong
        if r.status == 404:
            e = discord.Embed(
                description=f"{redmark} __*{ctx.author.mention}, something went wrong when trying to get the tv shows*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
          
        #Make embed
        e = discord.Embed(
            description=f"*Showing Info for {m['name']} - Ranked* **#{page_num}**")
        
        #Make fields
        fields = [
                ("🔗 __*Misc Info*__", 
                
                f"Genre IDS -> {m['genre_ids']}" +
                f"\nOrigin (Country) -> {m['origin_country']}" +
                f"\nOriginal Lang. -> {m['original_language']}" +
                f"\nMovie ID -> {m['id']}", False), 
                
                ("⬆️ __*Votes*__", 
                
                f"Total Votes -> {m['vote_count']}" +
                f"Vote Average -> {m['vote_average']}", False), 
                
                ("__*Overview*__", m['overview'], True)]
                
        #Add fields
        for n, v, i in fields:
            e.add_field(
                name=n, 
                value=v, 
                inline=i)
        
        #Set author
        e.set_author(
            name=f"Page {p}/{totalp}\nTotal Results : {totalr}")
        
        #Make the thumbnail the tv show cover
        e.set_thumbnail(
            url=f"https://image.tmdb.org/t/p/w500/{m['poster_path']}")
        
        #Set footer
        e.set_footer(
            text=f"Requested by {ctx.author}")
        
        #Send embed
        await ctx.send(embed=e)

    @command(
      brief="{Get a List of Guilds the Bot's in}", 
      usage="bguilds", 
      aliases=['botguilds'])
    @guild_only()
    @is_owner()
    async def bguilds(self, ctx):

        #Empty String 
        #To add guild names later
        g_list = ''
        
        #Iterate through servers bot's in
        for g in self.bot.guilds:
            
            name_owner = f"{g.name} **{{{len(g.members)} Mem}}** - {g.owner}"
            #Add the guild names
            #To the empty string
            g_list += f'• {"".join(name_owner)}\n'

        #Make embed
        e = discord.Embed(
            title=f"__*Total Guilds {{{len(self.bot.guilds)}}}*__", 
            description=g_list)
        
        e.timestamp = datetime.utcnow()
        
        e.set_footer(
            text=ctx.author, 
            icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=e)

    @command(
        name='reload', 
        brief="{Reloads all/specificied cog(s)", 
        usage="reload (cog_name)")
    @guild_only()
    @is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                e = discord.Embed(
                    title="Reloading all cogs!",
                    timestamp=datetime.utcnow())
                    
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            
                            e.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=True)

                        except Exception as e:
                            e.add_field(
                                name=f"__*Failed to reload*__ ``{ext}``",
                                value=e,
                                inline=True)
                                
                        await asyncio.sleep(0.5)
                await ctx.send(embed=e)
        else:
            # reload the specific cog
            async with ctx.typing():
              
                e = discord.Embed(
                    title="__*Reloading all cogs*__",
                    timestamp=datetime.utcnow())
                    
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    e.add_field(
                        name=f"__*Failed to reload*__ ``{ext}``",
                        value="This cog doesn't exist",
                        inline=True)

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                      
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        e.add_field(
                            name=f"__*Reloaded*__ ``{ext}``",
                            value='\uFEFF',
                            inline=True)
                            
                    except Exception:
                      
                        trace = traceback.format_exc()
                        
                        if len(trace) > 850:
                            length = len(trace) - 850
                            
                            trace = f"```{trace[:850]}``` and **{length}** more words..."
                        
                        else:
                            trace = f"```{trace}```"
                        
                        e.add_field(
                            name=f"__*Failed to reload*__ ``{ext}``",
                            value=trace,
                            inline=True)
                            
                await ctx.send(embed=e)

    @command(
        brief="{Load all/specific cogs}", 
        usage="load (cog_name)")
    @guild_only()
    @is_owner()
    async def load(self, ctx, cog=None):
        #If a cog isn't given
        #Load all the cogs
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                e = discord.Embed(
                    title="__*Reloading all cogs*__",
                    timestamp=datetime.utcnow())
                  
                #Iterate through the cog files
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            #Load the cog(s)
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            
                            e.add_field(
                                name=f"__*Reloaded*__ ``{ext}``",
                                value='\uFEFF',
                                inline=True)
                                
                        except Exception as e:
                            e.add_field(
                                name=f"__*Failed to load in*__ ``{ext}``",
                                value=e,
                                inline=True)
                                
                        await asyncio.sleep(0.5)
                await ctx.send(embed=e)
        else:
            #Load the specific cog
            async with ctx.typing():
                e = discord.Embed(
                    title=f"__*Loading in*__ ``{cog}``",
                    timestamp=datetime.utcnow())
                    
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                  
                    # if the file does not exist
                    e.add_field(
                        name=f"__*Failed to load in*__ ``{ext}``", 
                        value="This cog doesn't exist",
                        inline=True)

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        #Load the cog(s)
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        
                        e.add_field(
                            name=f"__*Loaded*__ ``{ext}``",
                            value='\uFEFF',
                            inline=True)
                            
                    except Exception:
                        trace = traceback.format_exc()
                        
                        if len(trace) > 850:
                            length = len(trace) - 850
                            
                            trace = f"```{trace[:850]}``` and **{length}** more words..."
                        
                        else:
                            trace = f"```{trace}```"
                        
                        e.add_field(
                            name=f"__*Failed to load*__ ``{ext}``",
                            value=trace,
                            inline=True)
                            
                await ctx.send(embed=e)

    @command(
        brief="{Unload a cog}", 
        usage="unload <cog_name>")
    @guild_only()
    @is_owner()
    async def unload(self, ctx, cog):
        #Unload the specific cog
        async with ctx.typing():
            e = discord.Embed(
                title=f"__*Unloading*__ ``{cog}``",
                timestamp=datetime.utcnow())
                
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                #If the file doesn't exist
                e.add_field(
                    name=f"__*Failed to Unload*__ ``{ext}``",
                    value="This cog doesn't exist",
                    inline=True)

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    #Unload the cog
                    self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        
                    e.add_field(
                        name=f"__*Unloaded*__ ``{ext}``",
                        value='\uFEFF',
                        inline=True)
                            
                except Exception:
                    desired_trace = traceback.format_exc()
                        
                    e.add_field(
                        name=f"__*Failed to reload*__ ``{ext}``",
                        value=desired_trace,
                        inline=True)
                            
            await ctx.send(embed=e)


            
    @command(
        brief="{Shutdown the Bot}", 
        usage="shutdown", 
        aliases=['logout', 'turnoff'])
    @is_owner()
    @guild_only()
    async def shutdown(self, ctx):
        
        await ctx.send("I'm shutting down now 👋🏽")
        
        await asyncio.sleep(1)
        
        #Makes bot logout
        await self.bot.logout()

#•----------Setup/Add this Cog----------•#
def setup(bot):
    bot.add_cog(Owner(bot))
