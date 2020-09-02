#•----------Modules----------•#
from aiohttp import ClientSession

import asyncio

import base64

import concurrent.futures

import discord

import json

from datetime import datetime

from random import choice, randint

from typing import Optional, Union

import random

import socket

from discord.ext.commands import command, BucketType, bot_has_permissions, guild_only, \
cooldown, Cog, is_owner

from MojangAPI import Client, DataService

from functools import partial

from mcstatus import MinecraftServer

from pyraklib.protocol.EncapsulatedPacket import EncapsulatedPacket

from pyraklib.protocol.UNCONNECTED_PING import UNCONNECTED_PING

from pyraklib.protocol.UNCONNECTED_PONG import UNCONNECTED_PONG

#•----------Class----------•#

class Minecraft(Cog, name="Minecraft Category"):

    def __init__(self, bot):
        self.bot = bot

        #Define our aiohttp ClientSession
        #To make apis easier to access
        self.ses = ClientSession(loop=self.bot.loop)

        self.g = self.bot.get_cog("Global")

        with open("data/build_ideas.json", "r") as stuff:
            _json = json.load(stuff)
            self.first = _json["first"]
            self.pronouns = _json["prenouns"]
            self.nouns = _json["nouns"]
            self.colors = _json["colors"]
            self.sizes = _json["sizes"]
            
#•----------Functions-----------•#
    
    #Run the ClientSession
    #Then close the session when complete
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
        name='mcping', 
        brief="{Check Status of a MC Server}", 
        usage="mcping <server_ip>",
        aliases=['serverping', 'mcstatus'])
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    async def mcping(self, ctx, host, port: int = None):
        
        port_str = ''
        if port is not None:
            port_str = f':{port}'
        combined = f'{host}{port_str}'

        async with ctx.typing():
            #Get the status from api
            res = await self.ses.get(f'https://theapi.info/mc/mcping?host={combined}') 
            jj = await res.json()

        if jj['online'] is not True:
            e = discord.Embed(
                color=0x420000, 
                title=f'<:offline:728377784207933550> {combined} is offline')
            await ctx.send(embed=e)
            return

        player_list = jj.get('players_names', [])  # list
        if player_list is None:
            player_list = []

        players_online = jj['players_online']  # int

        e = discord.Embed(
            color=randint(0, 0xffffff), 
            title=f'<:online:728377717090680864> {combined} is online', 
            description=f"*Version:* {jj['version'].get('brand', 'Unknown')}")

        e.add_field(
            name='__*Latency/Ping*__', 
            value=jj['latency'])

        player_list_cut = player_list[:24]

        if jj['version']['method'] != 'query' and len(player_list_cut) < 1:
            e.add_field(
                name=f'__*Online Players ({players_online}/{jj["players_max"]})*__',
                value='*Player list is not available for this server*',
                inline=True)
                
        else:
            extra = ''
            if len(player_list_cut) < players_online:
                extra = f', and {players_online - len(player_list_cut)} others...'

            e.add_field(
                name=f'__*Online Players ({players_online}/{jj["players_max"]})*__',
                value='`' + '`, `'.join(player_list_cut) + '`' + extra,
                inline=False)

        e.set_image(
            url=f'https://theapi.info/mc/mcpingimg?host={combined}&imgonly=true&v={random.random()*100000}')

        if jj['favicon'] is not None:
            e.set_thumbnail(
                url=f'https://theapi.info/mc/serverfavi?host={combined}')

        await ctx.send(embed=e)

    @command(
        brief="{Get a User's Skin}", 
        usage="skin <player/uuid>", 
        aliases=['stealskin', 'mcskin'])
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    @bot_has_permissions(use_external_emojis=True, embed_links=True)
    async def skin(self, ctx, *, gamertag: str):
        
        #Define author to make stuff shorter
        mem = ctx.author
        
        redmark = "<:redmark:738415723172462723>"
      
        response = await self.ses.get(f"https://api.mojang.com/users/profiles/minecraft/{gamertag}")
        
        #If there is no player found
        if response.status == 204:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, That Player doesn't Exist*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
        
        #Try to find the uuid of the playwer 
        uuid = json.loads(await response.text()).get("id")
        #If there is no uuid
        if uuid is None:
            e = discord.Embed(
                color=0x420000, 
                description=f"{redmark} __*{mem.mention}, That player doesn't exist*__")
            await ctx.send(embed=e)
            return

        response = await self.ses.get(
            f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}?unsigned=false")
            
        content = json.loads(await response.text())
        if "error" in content:
            if content["error"] == "TooManyRequestsException":
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, You have to Slow Down*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
              
        if len(content["properties"]) == 0:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, This user's skin can't be stolen for some reason*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
          
        undec = base64.b64decode(content["properties"][0]["value"])
        try:
            #Get the download url of the skin
            skin_download = json.loads(undec)["textures"]["SKIN"]["url"]
        except Exception:
            e = discord.Embed(
                color=0x420000, 
                description=f"{redmark} __*An error occurred while fetching that skin*__")
                
            await ctx.send(embed=e)
            return
        
        #Get user's uuid
        uuid = await self.ses.post("https://api.mojang.com/profiles/minecraft", json=[gamertag])
        j = json.loads(await uuid.text())
        
        #If uuid isn't found/doesn't exist
        if not j:
            e = discord.Embed(
                description=f"{redmark} __*That user couldn't be found*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
        
        #Shows the head of the skin
        skin_head = f"https://minotar.net/avatar/{gamertag}/50.png"
        
        #Make embed
        e = discord.Embed(
            title=f"*Download Here*", 
            url=skin_download, 
            description=f"__*UUID*__ -> {j[0]['id']}")
        
        #A dict for us to choose a random response
        ran = [
          f"{gamertag}'s Epic Skin", 
          f"{gamertag}'s Awesome Skin",
          f"{gamertag}'s Sexy Skin"
          ]
        
        e.set_author(
            name=choice(ran), 
            icon_url=skin_head)

        e.set_footer(
            text=f"Requested by {mem}")
                
        #Set embed image as skin's body
        e.set_image(
            url=f"https://mc-heads.net/body/{gamertag}/110")
            
        #Send embed
        await ctx.send(embed=e)
        
    @command(
        brief="{Get a List of Name History on MC Player}", 
        usage="names <player/uuid>", 
        aliases=['namehistory', 'namelist'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def names(self, ctx, *, gamertag: str):
      
        #Define custom emoji as a var
        redmark = "<:redmark:738415723172462723>"
        
        garbage = "<:trash:734043301187158082>"
        
        #Defining author as something easier
        mem = ctx.author
        
        #Aiohttp session to get a player's username
        r = await self.ses.post(f"https://api.mojang.com/profiles/minecraft", json=[gamertag])
        j = json.loads(await r.text())
        
        #If a user with that name isn't found
        if not j:
            e = discord.Embed(
                color=0x420000, 
                description=f"{redmark} __*{mem.mention}, That Player Couldn't be Found*__")
            await ctx.send(embed=e)
            return
        
        #Get the api for our embed
        res = await self.ses.get(
            f"https://some-random-api.ml/mc?username={gamertag}")
        
        #Storing the aiohttp session as a var
        mn = await res.json()
        #Define the dict/json we're getting
        data = mn
        
        #Change 'origanal' in the api
        #To 'original'
        data['name_history'][0]['changedToAt'] = "Original Name"
        
        #Change case where month is 0
        data['name_history'][3]['changedToAt'] = "1/29/2017"
        
        #Store the user name history
        #As a variable
        history = data['name_history'][::-1]
            
        #Split the names into chunks of 3
        #name_chunks = [history[i:i + 3] for i in range(0, len(history), 3)]
          
        #Max number of pages we can have
        page_max = len(history)
            
        #Start the pages (Defaults to first {1})
        page = 1
            
        #Empty list to store the embed fields later on
        embed_list = []
        
        #Make a variable we will add on to later
        num = 0
        #Reverse all the numbers
        num_list = list(range(len(history)))[::-1]
        
        #Iterate through the list of dicts
        for item in history:
            #Empty list of name fields
            nfields = []
                
            username = item['name']
            user_date = item['changedToAt']
            #Check to make sure we don't count
            #Original name
            if item['changedToAt'] == "Original Name":
                namedate = user_date
            else:
                namedate = datetime.strptime(user_date, "%m/%d/%Y").strftime('%a/%b %d/%Y')
            
            #Add these fields to our empty list
            #Of name fields above
            nfields.append((
                    "•------------------•", 
                    
                    f"**{num_list[num]+1}.** `{username}` - {namedate}", True))
            
            e = discord.Embed(
                description=f"**{gamertag}'s Name History**", 
                timestamp=datetime.utcnow())

            fields = nfields
                     
            #Add fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
                    
            #The skin's head as a link/png
            skin_head = f"https://minotar.net/avatar/{gamertag}/50.png"
        
            #Set the embed author
            e.set_author(
                name=f"Page {page}/{page_max}")

            e.set_footer(
                text=f"Ordered by Most Recent to Oldest")

            e.set_thumbnail(
                url=f"https://minotar.net/bust/{gamertag}/100.png")
            
            #Add this embed to our empty list of embeds
            embed_list.append(e)
                
            #Add to the number variable above
            num += 1 
                
            #Add to the page variable
            page += 1
            
        #Default pages to first page {1}
        page = 1
                
        #Send embed
        m = await ctx.send(embed=embed_list[page-1])
            
        #List of reactions to add
        react = ['⬅️', '➡️', '⏹']
        #Add the reactions
        for emotes in react:
            await m.add_reaction(emotes)
        
        #Custom check for when checking user reactions
        def checkauth(reaction, user):
            return user == ctx.author and reaction.message.id == m.id and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            except asyncio.TimeoutError:
                e = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react", 
                    color=0x420000)
                await m.edit(embed=e)
                await m.clear_reactions()
                #Break the loop
                break
            
            else:
                if str(reaction.emoji) == '➡️' and page != page_max:
                    await m.remove_reaction(reaction, user)
                    page += 1
                    #Edit the original embed with
                      #Our list of embeds
                    await m.edit(embed=embed_list[page-1])

                elif str(reaction.emoji) == '⬅️' and page > 1:
                    await m.remove_reaction(reaction, user)
                    
                    page -= 1
                    #Edit original embed
                    #With list of embeds
                    await m.edit(embed=embed_list[page-1])
                
                elif str(reaction.emoji) == '⏹':
                    
                    await m.clear_reactions()
                    
                    em = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    
                    await m.edit(embed=em, delete_after=5)
              
                else:
                    await m.remove_reaction(reaction, user)
            
        #except KeyError:
            #e = discord.Embed(
                #description=f"{redmark} __*{mem.mention}, that isn't a Valid Player*__", 
                #color=0x420000)
            #await ctx.send(embed=e)
            #return
      
    @command(
        brief="{See a Player's Cape}", 
        usage="cape <player/uuid>")
    @is_owner()
    @guild_only()
    async def cape(self, ctx, *, gamertag: str):
        
        #Make a custom emoji a variable
        redmark = "<:redmark:738415723172462723>"
        
        #Define the author as something shorter
        mem = ctx.author
        
        async with ctx.typing():
            r = await self.ses.post("https://api.mojang.com/profiles/minecraft", json=[gamertag])
        
            j = json.loads(await r.text())
            #If a user couldn't be found
            if not j:
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, that isn't a valid player*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
        
            #Use the MojangAPI 
            #To search for a mc user's cape
            user = await Client.User.createUser(gamertag)
            cape = await user.getProfile()
            print(cape)

            #If there isn't a cape for that player
            if cape.cape is None:
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, **{gamertag}** doesn't have a cape*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
        
            #List of random choices we want to get    
            ran = [
              f"{gamertag}'s Epic Cape", 
          
              f"{gamertag}'s Awesome Cape", 
              f"{gamertag}'s Sexy Cape"]
            
            e = discord.Embed()

            #Set the author name as a random choice
            #From the list above
            e.set_author(
                name=choice(ran), 
                icon_url=f"https://minotar.net/avatar/{gamertag}")
        
            #Set the image as the user's cape
            e.set_image(
                url=cape.cape)
        
            e.set_footer(
                text=mem)
            e.timestamp = datetime.utcnow()
        
            await ctx.send(embed=e)
        
    @command(
        name="uuid", 
        brief="{Get a UUID with a Username}",
        usage="uuid <player>", 
        aliases=[''])
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    @bot_has_permissions(embed_links=True, use_external_emojis=True)
    async def get_uuid(self, ctx, *, gamertag: str):
        
        redmark = "<:redmark:738415723172462723>"
        
        #Makes stuff shorter
        mem = ctx.author
        
        #If the user tries to use a uuid
        if len(gamertag) > 30:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, you can't use uuid's*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
        
        try:
            #Get the api
            r = await self.ses.post("https://api.mojang.com/profiles/minecraft", json=[gamertag])
        
            #j[0]['id'] \/
            j = json.loads(await r.text())  
            #If a user couldn't be found
            if not j:
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, that isn't a Valid Player*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
          
            #Make the embed to send
            e = discord.Embed(
                title="Search UUID's here", 
                url="https://mcuuid.net", 
                description=f"\n*UUID for **{gamertag}** -> {j[0]['id']}*\n\n")
        
            e.set_thumbnail(
                url=f"https://minotar.net/bust/{gamertag}/100.png")
        
            e.set_footer(
                text=f"Requested by {mem}")
            e.timestamp = datetime.utcnow()
        
            #Send embed
            await ctx.send(embed=e)
            
        except KeyError:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, that isn't a Valid Player", 
                color=0x420000)
            await ctx.send(embed=e)

    @command(
        name="mcplayer", 
        brief="{Get a Gamertag using a UUID}", 
        usage="mcplayer <uuid>", 
        aliases=['gamertag', 'mcuser', 'mcname'])
    @cooldown(1, 2.5, BucketType.user)
    @guild_only()
    @bot_has_permissions(embed_links=True, use_external_emojis=True)
    async def get_gamertag(self, ctx, *, uuid):
        
        #Define our custom emoji
        redmark = "<:redmark:738415723172462723>"
        
        #Define author as something easier
        mem = ctx.author
        
        #Check if a uuid is given
        #uuid's are over 30 characters
        if len(uuid) < 30:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, That isn't a Valid MC UUID*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
        
        try: 
            #Get the api
            response = await self.ses.get(f"https://api.mojang.com/user/profiles/{uuid}/names")
        
            #If a player isn't valid
            if response.status == 204:
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention}, That Player doesn't exist*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
        
            #Get the name 
            j = json.loads(await response.text())
            name = j[len(j) - 1]["name"]
        
            #Make the embed
            e = discord.Embed(
                title="Convert UUID's to Players Here", 
                url="https://mcuuid.net", 
                description=f"*Name for **{uuid}** -> {name}*")
        
            #Set the thumbnail as player's skin
            #Just for aesthetics yk
            e.set_thumbnail(
                url=f"https://minotar.net/bust/{uuid}/100.png")
        
            e.set_footer(
                text=f"Requested by {mem}")
            e.timestamp = datetime.utcnow()
        
            #Send embed
            await ctx.send(embed=e)
            
        #If the uuid doesn't match a player
        except KeyError:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, that isn't a Valid Player*__", 
                color=0x420000)
            await ctx.send(embed=e)
        
    @command(
        brief="{Converts your Text into Villager Noises}", 
        usage="villagerspeak <text>", 
        aliases=['vspeak'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def villagerspeak(self, ctx, *, msg):
        
        #Use the function/method from above 
        #To convert user's text
        await self.lang_convert(ctx, str(msg).replace("\\", "\\\\"), self.g.villagerLang)
    
    @command(
        brief="{Converts text into Enchantment Table Language}", 
        usage="enchant <text>")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def enchant(self, ctx, *, msg):
        msg = str(msg).replace("```", "").replace("\\", "\\\\")
        await self.lang_convert(ctx, "```" + msg + "```", self.g.enchantLang)
        
    @command(
        brief="{Unenchant text}", 
        usage="unenchant <enchantment_text>", 
        aliases=['unchant'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def unenchant(self, ctx, *, msg):
        lang = {}
        
        for key in list(self.g.enchantLang):
            lang[self.g.enchantLang[key]] = key
        await self.lang_convert(ctx, str(msg), lang)
        
    @command(
        brief="{Get a Random Cursed Minecraft Image}", 
        usage="cursed", 
        aliases=['mccursed', 'cursedmc'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def cursed(self, ctx):
        #Get the images from 'global.py'
        images = self.g.cursedImages
        
        e = discord.Embed(
            color=randint(0, 0xffffff))
            
        e.set_image(
            url="http://olimone.ddns.net/images/cursed_minecraft/" + random.choice(images))
        
        await ctx.send(embed=e)
        
    @command()
    @is_owner()
    async def testmc(self, ctx):
        
        dung = await DataService.Data.getStatistics(item_sold_dungeons=True)

        mc = await DataService.Data.getStatistics(item_sold_minecraft=True)

        #Make the embed
        e = discord.Embed(
            color=randint(0, 0xffffff), 
            title="Total Sales for Minecraft")
        
        #Make our fields
        fields = [
                  ("__*Total Minecraft Copies*__", 
                  f"Total: **{mc['total']}** Total Copies" +
                  f"\nSold last **24** Hours: {mc['last24h']}" +
                  f"\nSold per Second: **{round(mc['saleVelocityPerSeconds'], 3)}** Copies sold a Sec", True), 
                  
                  ("__*Minecraft Dungeon Sales*__", 
                  f"Total: **{dung['total']}**" +
                  f"\nSold Last **24** Hours: **{dung['last24h']}** Sold", True)
                  ]
        
        #Add our fields
        for n, v, i in fields:
            e.add_field(
                name=n, 
                value=v, 
                inline=i)
          
        #Send embed
        await ctx.send(embed=e)

    @command(
        name="mcsales", 
        brief="{Get the Total Sales on Minecraft}", 
        usage="mcsales")
    @guild_only()
    @cooldown(1, 1, BucketType.user)
    async def mc_sales(self, ctx):

        r = await self.ses.post("https://api.mojang.com/orders/statistics",
                                json={"metricKeys": ["item_sold_minecraft", "prepaid_card_redeemed_minecraft"]})
        j = json.loads(await r.text())
        await ctx.send(embed=discord.Embed(color=discord.Color.dark_green(),
                                           description=f"**{j['total']}** total Minecraft copies sold, **{round(j['saleVelocityPerSeconds'], 3)}** copies sold per second."))

    @command(
        name="randomserver", 
        brief="{Get a Random Minecraft Server}", 
        usage="randomserver", 
        aliases=['mcserver'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def random_mc_server(self, ctx):
      
        #Define a variable
        #For getting a random choice from mc server.json
        s = choice(self.g.mc_servers)
        
        try:
            #If the server's online
            #Use online custom emoji
            online = MinecraftServer.lookup(s['ip'] + ":" + str(s['port'])).status()
            stat = "<:online:728377717090680864>"
          
        #If the server's offline
        #Use an offline custom emoji
        except Exception:
            stat = "<:offline:728377784207933550>"
        
        #Make it look like the bot's typing in chat
        #In case it takes long to send the embed
        async with ctx.typing():
          
            mark = "<:greenmark:738415677827973152>" if s['verified'] is True else "<:redmark:738415723172462723>"
            
            #Make embed
            e = discord.Embed(
                timestamp=datetime.utcnow(), 
                description=f"*Status for **{s['name']}** -> {stat}*")
            
            #Make fields
            fields = [
                    ("__*Server IP*__", s['ip'], True), 
                    
                    ("__*Server Port*__", s['port'], True), 
                    
                    ("__*Version*__",  
                    f"{s['version']}{{{s['type']}}}", True), 
                    
                    ("__*Verified?*__", 
                    f"{mark} {s['verified']}", True)
                    ]
            
            #Add the fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
            e.set_footer(
                text=f"Requested by {ctx.author}")
                
            e.set_thumbnail(
                url=s['image'])
        
            #Send embed
            await ctx.send(embed=e)
            
    @command(
        name="mcidea", 
        brief="{Get a Random Build Idea}", 
        usage='mcidea', 
        aliases=['buildidea'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def build_idea(self, ctx):
      
        if choice([True, False]):
            e = discord.Embed(
                description=f"*{choice(self.first)} {choice(self.pronouns)}{choice(['!', ''])}*", 
                color=randint(0, 0xffffff))
            await ctx.send(embed=e)
            
        else:
            e = discord.Embed(
                description=f"*{choice(self.first)} a {choice(self.sizes)}, {choice(self.colors)} {choice(self.nouns)}{choice(['!', ''])}*", 
                color=randint(0, 0xffffff))
            await ctx.send(embed=e)

    @command(
        name="mccolors", 
        brief="{Colorcodes for Minecraft Text}", 
        usage="mccolors", 
        aliases=['mccolorcodes'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def mc_color_codes(self, ctx):
      
        #Define author as something easier
        mem = ctx.author
        
        #Make our embed
        e = discord.Embed(
            description="*Text in Minecraft can be formatted using different codes and using the {``§``} sign*")
        
        #Set the embed author  
        e.set_author(
            name="Minecraft Text Color Formatting")
        
        #Make our fields
        fields = [("__*Bright Colors*__", 
                  "<:red:749067570379882496> **Red** ``§c``" +
                  
                  "\n<:yellow:749080901253857331> **Yellow** ``§e``" +
                  
                  "\n<:green:749080915082215454> **Green** ``§a``" +
                  
                  "\n<:aqua:749108387093938177> **Aqua** ``§b``" +
                  
                  "\n<:blue:749080929552695428> **Blue** ``§9``" +
                  
                  "\n<:light_purple:749102028046729266> **Light Purple** ``§d``\n" +
                  
                  "\n<:white:749101731136274502> **White** ``§f``" +
                  
                  "\n<:lightgray:749101578014687343> **Gray** ``§7``", True), 
                  
                  ("__*Dark Colors*__", 
                  "<:dark_red:749101827995205642> **Dark Red** ``§4``\n" +
                  
                  "<:darkyellow:749102067750010884> **Gold** ``§6``\n" +
                  
                  "<:darkgreen:749101908911980678> **Dark Green** ``§2``\n" +
                  
                  "<:dark_aqua:749108577180057650> **Dark Aqua** ``§3``\n" +
                  
                  "<:darkblue:749101874338201601> **Dark Blue** ``§1``\n" +
                  
                  "<:darkpurple:749101989564121179> **Dark Purple** ``§5``\n" +
                  
                  "<:darkgray:749101943737155615> **Dark Gray** ``§8``\n" +
                  
                  "<:black:749102125224689676> **Black** ``§0``\n", True), 
                  
                  ("__*Formatting/Markdown*__", 
                  "<:bold:749106727353581619> **Bold** ``§l``\n" +
                  
                  "<:emoji_21:749106924225691658> ~~Strikethrough~~ ``§m``\n" +
                  
                  "<:underline:749106690774794250> __Underline__ ``§n``\n" +
                  
                  "<:italic:749105941214920766> *Italic* ``§o``\n" +
                  
                  "<:obfuscated:749106114662105139> ||Obfuscated|| ``§k``\n" +
                  
                  "<:reset:749108115039060050> Reset ``§r``\n", True)]
        
        #Add our fields
        for n, v, i in fields:
            e.add_field(
                name=n, 
                value=v, 
                inline=i)
        
        e.set_footer(
            text=f"Requested by {mem}", 
            icon_url=mem.avatar_url)
        
        #Send the embed
        await ctx.send(embed=e)

#•----------Setup/Add this Cog----------•#    
        
def setup(bot):
    bot.add_cog(Minecraft(bot))
