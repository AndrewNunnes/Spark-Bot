
#•----------Modules-----------•#
import discord

from discord.ext.commands import BucketType, has_permissions, bot_has_permissions, \
guild_only, cooldown, Cog, command, MissingRequiredArgument

from discord import Spotify

import typing

import asyncio

from random import choice, randint

from datetime import datetime

from aiohttp import ClientSession

import aiohttp

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
        
#•----------Methods----------•#

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
      brief="{Shows a Menu for Minecraft Commands}", 
      usage="minecraft")
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    async def minecraft(self, ctx):
      
      #Defining the author
      #Makes stuff shorter
      mem = ctx.author
      
      #Get the cog by it's class
      #Using a function from another file
      cog = self.gc.get_cog_by_class('Minecraft')
      
      #Make embed
      e = discord.Embed(
        title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__")
      
      #Iterate through the Subcommands
      for c in cog.walk_commands():
          
          #Make fields
          fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", 
                    c.brief, True)]
          
          #Add fields
          for n, v, i in fields:
              e.add_field(
                  name=n, 
                  value=v, 
                  inline=i)
                  
      e.set_thumbnail(
          url=mem.avatar_url)
      e.set_footer(
          text=mem)

      e.timestamp = datetime.utcnow()
    
      await ctx.send(embed=e)
      
    @command(
        brief="{Insult a Member}",
        usage="insult <member>", 
        aliases=['bully'])
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    async def insult(self, ctx, member: discord.Member):
      
        if not member:
            await ctx.send("You have to give a member to insult")
            return
      
        #A dict for us to get a random choice from
        res = [
          f"{member.mention} you're so ugly", 
          f"{member.mention} Go Workout and do something with your life", 
          f"Most babies fell on the floor at birth, {member.mention}, you were thrown at the wall", 
          f"{member.mention} We both know your parents don't love you",
          f"{member.mention} if only there was a vaccine to fix your stupidity", 
          f"{member.mention} why do you still wear diapers bruh", 
          f"{member.mention} go take a shower, you smell like 💩", 
          f"{member.mention} Close your legs 🐠", 
          f"{member.mention} go jump off a cliff"
          ]
          
        #Make embed
        e = discord.Embed(
            description=f"**{random.choice(res)}**")
            
        #Send embed
        await ctx.send(embed=e)
        
    @command(
        brief="{Compliment a Member}", 
        usage="compliment <member>", 
        aliases=['comp', 'compl'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def compliment(self, ctx, member: discord.Member):
        
        #If the member isn't given
        if not member:
            await ctx.send("You have to give a member to compliment")
            return
        
        #A dict for us to go through
        res = [
          f"{member.mention} did you just get your nails done? They look clean 👻", 
          f"{member.mention} I see you're packing", 
          f"{member.mention} Nice fit 😎", 
          f"Damn {member.mention} is that a new watch? Niceee"
          ]
          
        #Make embed
        e = discord.Embed(
            description=f"**{random.choice(res)}**")
            
        #Send embed
        await ctx.send(embed=e)

    @command(
      brief="{Get a Random Meme}", 
      usage="meme")
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    async def meme(self, ctx):

        async with ctx.typing():
            url= "https://apis.duncte123.me/meme"
            ses = ClientSession()
            async with ses.get(url) as r:
                
                #Make this coroutine a variable
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
        
        formatted = pyfiglet.figlet_format(text)
        
        e = discord.Embed(
            description=f"```{formatted}```")
            
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
                
                e.description = f'{user.mention} is listening to: **{act.title}**'
                
                e.set_thumbnail(
                    url=act.album_cover_url)
                
                #Display the length of the song
                length = f"{pendulum.duration(seconds=act.duration.total_seconds()).in_words(locale='en')}"
                
                #Make fields
                fields = [("**Song Name**", act.title, True),
                
                          ("**Song Artist**", act.artist, True), 
                          
                          ("**Song's Album**", act.album, True), 
                          
                          ("**Length**", length, True)]
                
                #Send the embed
                await ctx.send(embed=e)
                
                #Break the loop
                break
        #If the user isn't listening
        #To anything
        else:
            e = discord.Embed(
                description=f"{user.mention} isn't listening to Spotify right now", 
                color=0x420000)
                
            await ctx.send(embed=e)
    
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

        async with ctx.typing():
            # Request profile information from API
            url = f"https://apis.duncte123.me/insta/{user_name}"
            async with aiohttp.ClientSession() as session:
                async with await session.get(url=url) as response:

                    # When succesful, read data from json
                    if response.status == 200:
                        insta = await response.json()

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

                        # When profile isn't private, grab the information of their last post
                        if not private:
                            image_url = images[0]["url"]
                            image_caption = images[0]["caption"]

                    #Send error if no instagram profile was found with given username
                    elif response.status == 422:
                        e = discord.Embed(
                            description=f"{redmark} __*{mem.mention}, that Account doesn't exist*__", 
                            color=0x420000)
                        
                        await ctx.send(embed=e)
                        return
                
                #Close the session
                await session.close()

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

    @insta.error
    async def insta_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            e = discord.Embed(
                description=f'❌ Please make sure to include the username\n```!insta <instagramhandle>```', 
                color=0x420000)
            
            e.set_author(
                name=f'{ctx.author}', 
                icon_url=f'{ctx.author.avatar_url}')
            
            await ctx.send(embed=e)
        else:
            raise(error)

    @command(
      brief="{Get a random fact}",
      usage="fact")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def fact(self, ctx):
      
        url = f'https://uselessfacts.jsph.pl/random.json?language=en'
        async with ClientSession() as session:
            async with session.get(url) as response:
              
                r = await response.json()
                
                fact = r['text']
                
                e = discord.Embed(
                    title=f'Random Fact', 
                    colour=random.randint(0x000000, 0xffffff))
                
                #Make fields
                fields = [(
                        "**Fun Fact**", 
                        fact, False)]
                
                #Add fields    
                for n, v, i in fields:
                    e.add_field(
                        name=n, 
                        value=v, 
                        inline=i)
                
                #Send embed
                await ctx.send(embed=e)
                
#•----------Setup/Add this Cog-----------•#

def setup(bot):
    bot.add_cog(Fun(bot))
