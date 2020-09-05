
#•----------Modules-----------•#
import discord

from discord.ext.commands import BucketType, has_permissions, bot_has_permissions, \
guild_only, cooldown, Cog, command, MissingRequiredArgument, is_owner

from discord import Spotify

import typing

import asyncio

from random import choice, randint

from datetime import datetime

from aiohttp import ClientSession

import os

import sys

import discord.utils

from discord import Game

import json

import pendulum

import pyfiglet

#•----------Class-----------•#

class Fun(Cog, name="Fun Category"):

    """`{Full List of Fun Commands}`"""

    def __init__(self, bot):
        self.bot = bot
        
        #Used to get the functions
        #From this cog
        self.gc = self.bot.get_cog('Helpdude')
        
        self.d = self.bot.emojified
        
        self.g = self.bot.get_cog('Global')
        
        self.ses = ClientSession(loop=self.bot.loop)
        
#•----------Methods/Functions----------•#

    #Used to run the ClientSession
    #And close when complete
    def cog_unload(self):
        self.bot.loop.create_task(self.ses.close())

    async def nice(self, ctx):
        com_len = len(f'{ctx.prefix}{ctx.invoked_with} ')
        return ctx.message.clean_content[com_len:]
        
    #Goes through message and replaces all 
    #Instances of keys with their values in a dict
    async def lang_convert(self, ctx, msg, lang):
        
        keys = list(lang)
        
        #Iterate through list of 'lang' argument
        for k in keys:
            msg = msg.replace(k, lang[k])
            
        #If user's message is too long
        if len(msg) > 750:
            e = discord.Embed(
                description=f"<:redmark:738415723172462723> That message is too long to convert")
            await ctx.send(embed=e)
        else:
            await ctx.send(msg)

#•-----------Commands----------•#
    
    @command(
        brief="{Menu for Minecraft Commands what else?}", 
        usage="minecraft", 
        aliases=['mc', 'mcmenu', 'minecraftmenu'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def minecraft(self, ctx):
        
        garbage = "<:trash:734043301187158082>"
        redmark = "<:redmark:738415723172462723>"
        
        #Get the cog by it's class
        cog = self.gc.get_cog_by_class('Minecraft')
        
        #Get the commands and store as a variable
        c = cog.get_commands()

        #Split the commands into 2 pages
        first = c[:len(c)//2]
        second = c[len(c)//2:]

        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            title=cog.qualified_name, 
            description="*() - Optional\n<> - Required*", 
            timestamp=datetime.utcnow())
        
        for comm in first:
        
            fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.set_thumbnail(
            url=ctx.author.avatar_url)
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
                        title=f"{cog.qualified_name}", 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in first:
        
                        fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

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
                        title=cog.qualified_name, 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in second:
        
                        fields2 = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields2:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

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
        brief="{Insult a Member}",
        usage="roast <member>", 
        aliases=['bully'])
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    async def roast(self, ctx, member: discord.Member):
        
        async with ctx.typing():
            #Url for the api
            url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
            #Get the api
            r = await self.ses.get(url)
            #Convert into json format
            js = await r.text()
            resp = json.loads(js)
        
            #If the api is unavailable
            if r.status != 200:
                e = discord.Embed(
                    description=f"__*{member.mention}, something went wrong*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
        
            #Make embed  
            e = discord.Embed(
                description=f"**{member.mention}, {resp['insult']}**", 
                color=0x420000)
            #Send embed
            await ctx.send(embed=e)
            
    @command(
      brief="{Get a Random Meme}", 
      usage="meme")
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    async def meme(self, ctx):

        async with ctx.typing():
            #api we want to get
            url = "https://apis.duncte123.me/meme"
            #Fetch the api
            r = await self.ses.get(url)
            #Turn the api into a json for easy access
            res = await r.json()
            
            #Get the meme url
            meme_url = f"{res['data']['url']}"

            #Make embed
            e = discord.Embed(
                title="Meme Link", 
                url=meme_url, 
                timestamp=datetime.utcnow())
                
            #Set the embed's image 
            #With the meme's image
            e.set_image(
                url=res['data']['image'])
                
            #Get the title
            #Of the meme
            val = f"{res['data']['title']}"

            e.add_field(
                name="__*Quality Meme 👌*__", 
                value=val)

            await ctx.send(embed=e)

    @command(
        brief="{Info on a Movie}", 
        usage="movie <movie_title>", 
        aliases=['searchmovie'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def movie(self, ctx, *, title):
        
        try:
            redmark = "<:redmark:738415>"
            
            #Only works if you have an api key inside the website
            url = f"https://api.themoviedb.org/3/search/movie?api_key=91841633d0b2b91d9e313adcce2cc2c7&query={title}"
            r = await self.ses.get(url)
            resp = await r.json()
            
            #If the resource isn't available
            if r.status == 404:
                e = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, that movie doesn't exist*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return

            #Make embed
            e = discord.Embed(
                description=f"**General Info for {resp['results'][0]['title']}**")

            fields = [
                    ("__*Misc Info*__", 
                    f"PG13? {resp['results'][0]['adult']}" +
                    f"\nOriginal Language: {resp['results'][0]['original_language']}" +
                    f"\nMovie ID: {resp['results'][0]['id']}" +
                    f"\nGenre ID's: {resp['results'][0]['genre_ids']}" +
                    f"\nVote Count: {resp['results'][0]['vote_count']}" +
                    f"\nVote Average: {resp['results'][0]['vote_average']}", True), 
                    
                    ("__*Overview*__", resp['results'][0]['overview'], True)]
            
            #Add fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
            e.set_thumbnail(
                url=f"https://image.tmdb.org/t/p/w500/{resp['results'][0]['poster_path']}")
            
            #Set footer to when movie
            #Was released
            e.set_footer(
                text=f"{resp['results'][0]['title']} Released | {resp['results'][0]['release_date']}")
            
            #Send embed
            await ctx.send(embed=e)
        
        #If the given movie doesn't exist
        except Exception:
            e = discord.Embed(
                description=f"{redmark} __*{ctx.author.mention}, that isn't a movie*__", 
                color=0x420000)
            await ctx.send(embed=e)  
            return

    @command(
        brief="{See what song somebody's listening to}", 
        usage="spotify <member>")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def spotify(self, ctx, user: discord.Member=None):
      
        user = user or ctx.author
        
        #Iterate through user's activities
        for act in user.activities:
            if isinstance(act, Spotify):
              
                e = discord.Embed(
                    color=0x0F4707)
                
                e.description = f'__*{user.mention} is listening to*__ **{act.title}**'
                
                e.set_thumbnail(
                    url=act.album_cover_url)
                
                #Display the length of the song
                length = f"{pendulum.duration(seconds=act.duration.total_seconds()).in_words(locale='en')}"
                
                #Make fields
                fields = [("*Song Name*", f"**  **• {act.title}", False),
                
                          ("*Song Artist*", f"**  **• {act.artist}", False), 
                          
                          ("*Song's Album*", f"**  **•{act.album}", False), 
                          
                          ("*Length*", f"**  **• {length}", True)]
                          
                #Add fields
                for n, v, i in fields:
                    e.add_field(
                        name=n, 
                        value=v, 
                        inline=i)
                
                #Send the embed
                await ctx.send(embed=e)
                
            #If the user isn't listening
            #To anything
            else:
                e = discord.Embed(
                    description=f"__*{user.mention}, isn't listening to Spotify right now*__", 
                    color=0x420000)
                
                await ctx.send(embed=e)
                return
    
    @command(
        brief="{Hack a Member}", 
        usage="hack <member>", 
        aliases=['hck'])
    @guild_only()
    async def hack(self, ctx, member:discord.Member = None):
        
        #If a member isn't given
        if not member:
            await ctx.send("Please mention a member")
            return
        
        #Fake passwords to go through
        passwords = [
                  'imnothackedlmao', 
                  'sendnoodles63', 
                  'ilovenoodles', 
                  'icantcode', 
                  'christianmicraft', 
                  'server', 
                  'icantspell', 
                  'hackedlmao', 
                  'WOWTONIGHT', 
                  '69']
        
        #Fake ips to go through
        fakeips=[
                  '154.2345.24.743',
                  '255.255. 255.0', 
                  '356.653.56', 
                  '101.12.8.6053', 
                  '255.255. 255.0']
        
        #Random time to wait for
        sec = randint(1, 3)

        e = discord.Embed(
            title=f"**Hacking: {member.mention}** 0%...", 
            color=randint(0x000000, 0xffffff))
        
        m = await ctx.send(embed=e)
        
        await asyncio.sleep(sec)
        
        e = discord.Embed(
            title=f"Searching for contacts... {{19%}}", 
            color=randint(0x000000, 0xffffff))
        
        await m.edit(embed=e)
        
        await asyncio.sleep(sec)
        
        e = discord.Embed(
            title=f"Searching for any friends if there is any {{34%}}", 
            color=randint(0x000000, 0xffffff))
            
        await m.edit(embed=e)
        
        await asyncio.sleep(sec)
        
        e = discord.Embed(
            title=f"Getting IP... {{55%}}", 
            color=randint(0x000000, 0xffffff))
        
        await m.edit(embed=e)
        
        await asyncio.sleep(sec)
        
        e = discord.Embed(
            title=f"Got IP {random.choice(fakeips)} {{69%}}", 
            color=randint(0x000000, 0xffffff))
            
        await m.edit(embed=e)
        
        await asyncio.sleep(sec)
        
        e = discord.Embed(
            title=f"Getting password... {{84%}}", 
            color=randint(0x000000, 0xffffff))
        
        await m.edit(embed=e)
        
        await asyncio.sleep(sec)
        
        e = discord.Embed(
            title=f"Got password {random.choice(passwords)} {{99%}}", 
            color=randint(0x000000, 0xffffff))
        
        await m.edit(embed=e)
        
        await asyncio.sleep(sec)
        
        embed = discord.Embed(
            title=f"**Hacking: {member}** 100%", 
            color=randint(0x000000, 0xffffff))
            
        await m.edit(embed=embed)
        
        await asyncio.sleep(sec)
        
        embed = discord.Embed(title=f"{member} info ", description=f"*Email `{member}@gmail.com` Password `{random.choice(passwords)}`  IP `{random.choice(fakeips)}`*", color=random.randint(0x000000, 0xffffff))
        embed.set_footer(text="You've totally been hacked 😏")
        await m.edit(embed=embed)

    @command(
      brief="{Info on an Insta Acc}", 
      usage="insta <insta_username>", 
      aliases=['instagram'])
    @cooldown(1, 1, BucketType.user)
    async def insta(self, ctx, *, user_name):
      
        redmark = "<:redmark:738415723172462723>"
        
        mem = ctx.author

        async with ctx.typing():
            # Request profile information from API
            url = f"https://apis.duncte123.me/insta/{user_name}"
            r = await self.ses.get(url)
            
            #If the api's available/online
            if r.status == 200:

                #Convert api into a json
                #For easy access later on
                insta = await r.json()

                data = insta["user"]
                
                images = insta["images"]
                private = data["is_private"]
                verified = data["is_verified"]

                full_name = data["full_name"]
                username = data["username"]
                pfp = data["profile_pic_url"]

                followers = data["followers"]["count"]
                following = data["following"]["count"]
                uploads = data["uploads"]["count"]
                biography = data["biography"]

                #When profile isn't private, grab the information of their last post
                if not private:
                    image_url = images[0]["url"]
                    image_caption = images[0]["caption"]

                #Send error if no instagram profile was found with given username
            elif r.status == 422:
              
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, that Account doesn't exist*__", 
                    color=0x420000)
                        
                await ctx.send(embed=e)
                return
                  
            elif r.status == 429:
                e = discord.Embed(
                        description=f"{redmark} __*{mem.mention}, you're being **RateLimited**\nYou spammed the command too much*__", 
                        color=0x420000)
                await ctx.send(embed=e)
                return
                  
            # Setting bools to ticks/cross emojis
            verif = "<:greenmark:738415677827973152>" if verified else redmark
            priv = "<:greenmark:738415677827973152>" if private else redmark
            
            biography = biography if biography else "No Bio"

            # Set the page url to the last post or the profile based on privacy settings
            page_url = images[0]["page_url"] if not private else f"https://www.instagram.com/{username}/"

            desc = f"**Full Name:** {full_name}" \
                   f"\n**Bio:** {biography}" \
                   f"\n\n**Verified?:** {verif} | **Private?:** {priv}" \
                   f"\n**Following:** {following} | **Followers:** {followers}" \
                   f"\n**Upload Count:** {uploads}"
                   
            e = discord.Embed(
                title=f"{username}'s Instagram", 
                description=desc, 
                url=page_url, 
                colour=0x420000)
                
            e.set_thumbnail(
                url=pfp)
                
            e.set_footer(
                text=f"Requested By {ctx.author}", 
                icon_url=ctx.author.avatar_url)

            # When profile is not private, display the last post with the caption
            if not private:
                e.add_field(
                    name="My Latest Post", 
                    value=f"**Caption:** {image_caption}", 
                    inline=False)
                    
                e.set_image(
                    url=image_url)

        await ctx.send(embed=e)

    @command(
      brief="{Get a random fact}",
      usage="fact")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def fact(self, ctx):
        
        async with ctx.typing():
            url = f'https://uselessfacts.jsph.pl/random.json?language=en'
            response = await self.ses.get(url)

            r = await response.json()
                
            fact = r['text']
                
            e = discord.Embed(
                title=f'Random Fact', 
                colour=randint(0x000000, 0xffffff))
                
            #Make fields
            fields = [("**Fun Fact**", fact, False)]
                
            #Add fields    
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
                
            #Send embed
            await ctx.send(embed=e)

            
    @command(
        brief="{Get Lyrics for a Song}", 
        usage="lyrics <song_title>", 
        aliases=['songlyrics', 'lyric'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def lyrics(self, ctx, *, title):
        
        mem = ctx.author
        
        redmark = "<:redmark:738415723172462723>"
        
        async with ctx.typing():
          
            try:
                #Getting the url
                url = f"https://some-random-api.ml/lyrics?title={title}"
                r = await self.ses.get(url)
            
                #Converting into json for easy access
                resp = await r.json()
            
                #Making variables for the json keys
                song_image = resp['thumbnail']['genius']
                song_artist = resp['author']
                song_title = resp['title']
            
                song_lyrics = resp['lyrics']
                #If song lyrics are too long
                if len(song_lyrics) > 650:
                    #Subtract 650 characters
                    #From lyrics
                    length = len(song_lyrics) - 650
                
                    lyrics = f"{''.join(song_lyrics[:650])} and **{length}** more words..."
                #Else if lyrics are less than 650 characters
                else:
                    lyrics = song_lyrics
            
                lyric_link = resp['links']['genius']
            
                #If the api's down
                if r.status != 200:
                    e = discord.Embed(
                        description=f"{redmark} __*{mem.mention}, looks like something went wrong*__", 
                        color=0x420000)
                    await ctx.send(embed=e)
            
                #Make embed
                e = discord.Embed(
                    title=f"*Direct Link to Lyrics for -> {{{song_title}}}*", 
                    url=lyric_link)
            
                #Set thumbnail as song image
                e.set_thumbnail(
                    url=song_image)
            
                #Make fields 
                fields = [
                          ("__*Lyrics*__", lyrics, True), 
                          
                          ("__*Artist*__", song_artist, True)]
            
                e.set_footer(
                    text=f"Requested by {mem}")
          
                #Add fields
                for n, v, i in fields:
                    e.add_field(
                        name=n, 
                        value=v, 
                        inline=i)
            
                await ctx.send(embed=e)
            
            #If the song doesn't exist 
            except KeyError:
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, that isn't a song*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
        
    @command(
        brief="{Do Math}", 
        usage="math <math_stuff>")
    @guild_only()
    @cooldown(1, 1.25, BucketType.user)
    async def math(self, ctx):

        redmark = "<:redmark:738415723172462723>"

        mem = ctx.author
        
        try:
            problem = str(ctx.message.clean_content.replace(f"{ctx.prefix}math", ""))
            
            #If a problem isn't given
            if problem == "":
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, you need to put an actual problem", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
            
            #If the user's problem is too long
            if len(problem) > 500:
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, that problem's way too long", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
              
            problem = problem.replace("÷", "/").replace("x", "*").replace("•", "*").replace("=", "==").replace("π", "3.14159")
            
            #Iterate through a string of invalid
            #Chracters
            for letter in "abcdefghijklmnopqrstuvwxyz\\_@~`,<>?|'\"{}[]":
                
                #If any of those characters are in user's math
                if letter in problem:
                    e = discord.Embed(
                        description=f"{redmark} __*{mem.mention}, that math problem has invalid characters*__", 
                        color=0x420000)
                    await ctx.send(embed=e)
                    return
            #Make embed
            e = discord.Embed(
                timestamp=datetime.utcnow())

            #Make fields   
            fields = [
                     ("__*Problem Given*__", problem, True), 
            
                      ("__*Answer*__", 
                      f"{str(round(eval(problem), 4))}", True)
                      ]
            #Add the fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
            e.set_footer(
                text=mem, 
                icon_url=mem.avatar_url)
            
            #Send embed
            await ctx.send(embed=e)
            
        #If the problem is unsolvable
        except Exception:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, looks like something went wrong*__", 
                color=0x420000)
            await ctx.send(embed=e)

    @command(
        brief="{Say something in Sarcasm}", 
        usage="sarcastic <text>", 
        aliases=['sarcasm', 'sarc'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def sarcastic(self, ctx, *, text):
        
        text = await self.nice(ctx)
        
        if len(text) > 500:
            await ctx.send("That message is too long to convert")
            return
          
        caps = True
        sarc = ''
        
        for letter in text:
            if not letter == ' ': 
                caps = not caps
                
            if caps:
                sarc += letter.upper()
            else:
                sarc += letter.lower()
                
        await ctx.send(sarc)
        
    @command(
        brief="{Places a 👏 in between your Text}", 
        usage="clap <text>")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def clap(self, ctx, *, msg):
        
        clapped = '👏' + ' 👏 '.join((await self.nice(ctx)).split(' ')) + ' 👏'
        
        if len(clapped) > 900:
            await ctx.send("That message is too long to convert")
            return
            
        await ctx.send(clapped)
        
    @command(
        brief="{Emojify your Text}", 
        usage="emojify <text>", 
        aliases=['emofy'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def emojify(self, ctx, *, msg):
        
        #Letters to try and emojify
        letters = 'abcdefghijklmnopqrstuvwxyz'
        
        #Empty string to add onto later
        text = ''
        
        #Iterate through
        for letter in (await self.nice(ctx)).lower():
            #If the message given is in
            #The list of letters we made
            if letter in letters: 
                text += f':regional_indicator_{letter}: '
            #Else if they don't give any letters
            else:
                text += self.d.get(letter, letter) + ' '
        
        #If the user's message is too long      
        if len(msg) > 750:
            await ctx.send("Message can't be over 750 Characters")
        #Else if it isn't
        else:
            await ctx.send(msg)

    @command(
        brief="{Sends a bubblewrap}", 
        usage="bubblewrap (#x#)", 
        aliases=['bwrap'])
    @guild_only()
    @cooldown(1, 3, BucketType.user)
    async def bubblewrap(self, ctx, size=None):
        
        #If a size isn't given
        #Use a default
        if size is None:
            size = (10, 10,)
        #Else if a size IS given
        else:
            #Split the two numbers given
            size = size.split('x')
           
            #If the size given is less
            #Than 2 characters
            #Should be #x#
            if len(size) != 2:
                await ctx.send("That isn't a valid size\nExample size is: 10x10")
                return
            
            try:
                #Try to Convert the sizes given
                #Into a number
                size[0] = int(size[0])
                size[1] = int(size[1])
            #If it isn't a number
            #Send this ValueError
            except ValueError:
                await ctx.send("That isn't a valid size\nExample size is: 10x10")
                return
            
            #Iterate through the size
            for val in size:
                #Check if the user gives
                #A size that's too big
                if val < 1 or val > 12:
                    await ctx.send("The size must be between 1 and 12")
        
        #The letters users will see
        #When bubblewrapping
        bubble = '||***pop***||'
        
        #Make embed
        e = discord.Embed(
            description=f'{bubble*size[0]}\n'*size[1])
            
        #Send embed
        await ctx.send(embed=e)
        
    @command(
        brief="{See how big your Penis is}", 
        usage="pp", 
        aliases=['penis', 'ppsize', 'penissize', 'penisize'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def pp(self, ctx):
        
        #The response for the embed to send
        penis = f"8{'=' * randint(1,25)}D"
        #Multiplies our '=' by a random choice of 1-15
        
        #A list to go through
        first_list = [
          "Your pp", 
          "Your penis", 
          "Your package"
          ]
          
        #Get a random choice
        first = choice(first_list)
        
        #List of stuff to go through
        title_list = [
          "PP Analizer", 
          "PP Inspector", 
          "PP Rater"
          ]
          
        title = choice(title_list)
        
        #Make the embed
        e = discord.Embed(
            title=title, 
            description=f"*{first} {penis}*", 
            color=randint(0, 0xffffff))
        
        #Send the embed
        await ctx.send(embed=e)
        
    @command(
        brief="{See how gay you are}", 
        usage="gay", 
        aliases=['gayrater', 'gayrate'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def gay(self, ctx):
        
        #Makes stuff shorter
        mem = ctx.author
        
        #Our responses for the embed
        #To send
        res = [
              f"You're {randint(15, 125)}% Gay 🏳️‍🌈🏳️‍🌈🏳️‍🌈", 
              
              f"{mem.mention} Stop Being so Gay, you were rated {randint(15, 135)}% Gay 🏳️‍🌈🏳️‍🌈🏳️‍🌈"
              ]
              
        #Make embed
        e = discord.Embed(
            title="Gay Patrol 🔫", 
            description=choice(res), 
            color=randint(0, 0xffffff))
            
        #Send embed
        await ctx.send(embed=e)

    @command(
        brief="{Make your Message a Fancy Embed}", 
        usage="embed <message>")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def embed(self, ctx, *, d):
        
        #Define the author
        #Makes stuff shorter
        mem = ctx.author

        #Make embed
        e = discord.Embed(
            description=d)
        
        #Set the embed author 
        e.set_author(
            name=mem, 
            icon_url=mem.avatar_url)
        
        #Send embed
        await ctx.send(embed=e)
        
    @command(
        brief="{Turn your words into a Banner}", 
        usage="banner <text>")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def banner(self, ctx, *, text):
        
        #Used to format the user's text
        formatted = pyfiglet.figlet_format(text)
        
        e = discord.Embed(
            description=f"```{formatted}```")
            
        await ctx.send(embed=e)

                
#•----------Setup/Add this Cog-----------•#

def setup(bot):
    bot.add_cog(Fun(bot))
