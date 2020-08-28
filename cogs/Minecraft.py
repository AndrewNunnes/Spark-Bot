
#•----------Modules----------•#
import aiohttp

import asyncio

import base64

import concurrent.futures

import discord

import json

from datetime import datetime

from random import choice

import socket

from discord.ext import commands

from functools import partial

from mcstatus import MinecraftServer

from pyraklib.protocol.EncapsulatedPacket import EncapsulatedPacket

from pyraklib.protocol.UNCONNECTED_PING import UNCONNECTED_PING

from pyraklib.protocol.UNCONNECTED_PONG import UNCONNECTED_PONG

#•----------Class----------•#

class Minecraft(commands.Cog, name="Minecraft Category"):

    def __init__(self, bot):
        self.bot = bot

        #Define our aiohttp ClientSessio
        self.ses = aiohttp.ClientSession(loop=self.bot.loop)

        self.g = self.bot.get_cog("Global")

        with open("data/build_ideas.json", "r") as stuff:
            _json = json.load(stuff)
            self.first = _json["first"]
            self.prenouns = _json["prenouns"]
            self.nouns = _json["nouns"]
            self.colors = _json["colors"]
            self.sizes = _json["sizes"]
    
    #Run the ClientSession
    #Then close the session when complete
    def cog_unload(self):
        print("Cog unloded")
        self.bot.loop.run_until_complete(self.ses.close())

    def vanilla_pe_ping(self, ip, port):
        ping = UNCONNECTED_PING()
        ping.pingID = 4201
        ping.encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(0)
        try:
            s.sendto(ping.buffer, (socket.gethostbyname(ip), port))
            sleep(1)
            recvData = s.recvfrom(2048)
        except BlockingIOError:
            return False, 0
        except socket.gaierror:
            return False, 0
        pong = UNCONNECTED_PONG()
        pong.buffer = recvData[0]
        pong.decode()
        sInfo = str(pong.serverName)[2:-2].split(";")
        pCount = sInfo[4]
        return True, pCount

    def standard_je_ping(self, combined_server):
        try:
            status = MinecraftServer.lookup(combined_server).status()
        except Exception:
            return False, 0, None

        return True, status.players.online, status.latency

    async def unified_mc_ping(self, server_str, _port=None, _ver=None):
        if ":" in server_str and _port is None:
            split = server_str.split(":")
            ip = split[0]
            port = int(split[1])
        else:
            ip = server_str
            port = _port

        if port is None:
            str_port = ""
        else:
            str_port = f":{port}"

        if _ver == "je":
            # ONLY JE servers
            standard_je_ping_partial = partial(self.standard_je_ping, f"{ip}{str_port}")
            with concurrent.futures.ThreadPoolExecutor() as pool:
                s_je_online, s_je_players, s_je_latency = await self.bot.loop.run_in_executor(pool,
                                                                                              standard_je_ping_partial)
            if s_je_online:
                return {"online": True, "player_count": s_je_players, "ping": s_je_latency, "version": "Java Edition"}

            return {"online": False, "player_count": 0, "ping": None, "version": None}
        elif _ver == "api":
            # JE & PocketMine
            resp = await self.ses.get(f"https://api.mcsrvstat.us/2/{ip}{str_port}")
            jj = await resp.json()
            if jj.get("online"):
                return {"online": True, "player_count": jj.get("players", {}).get("online", 0), "ping": None,
                        "version": jj.get("software")}
            return {"online": False, "player_count": 0, "ping": None, "version": None}
        elif _ver == "be":
            # Vanilla MCPE / Bedrock Edition (USES RAKNET)
            vanilla_pe_ping_partial = partial(self.vanilla_pe_ping, ip, port if port is not None else 19132)
            with concurrent.futures.ThreadPoolExecutor() as pool:
                pe_online, pe_p_count = await self.bot.loop.run_in_executor(pool, vanilla_pe_ping_partial)
            if pe_online:
                return {"online": True, "player_count": pe_p_count, "ping": None, "version": "Vanilla Bedrock Edition"}
            return {"online": False, "player_count": 0, "ping": None, "version": None}
        else:
            tasks = [
                self.bot.loop.create_task(self.unified_mc_ping(ip, port, "je")),
                self.bot.loop.create_task(self.unified_mc_ping(ip, port, "api")),
                self.bot.loop.create_task(self.unified_mc_ping(ip, port, "be"))
            ]

            for task in tasks:
                while not task.done():
                    await asyncio.sleep(.05)

            for task in tasks:
                if task.result().get("online") is True:
                    return task.result()

            return {"online": False, "player_count": 0, "ping": None, "version": None}
            
    #@commands.command(brief="{Menu for Minecraft Commands}")
  #  async def minecraft(self, ctx):
      
    #  cog = self.bot.get_cog('Minecraft')
   #   commands = cog.get_commands()
      #command_desc = [c.short_doc for c in cog.walk_commands()]
   #   commandnames = [f"_*{c.name}*_ - `{c.brief}`" for c in cog.walk_commands()]
      
    #  e = discord.Embed(
   #     title=f"__*{cog.qualified_name}*__", 
    #    description="_*() - Optional\n<> - Required*_", 
      #  color=0x6F5913)
   #   e.add_field(
    #    name="_*Your Available Commands*_", 
    #    value="\n".join(commandnames))
   #   e.timestamp = datetime.datetime.utcnow()
      
    #  await ctx.send(embed=e)
      

    @commands.command(name="mcping", brief="{Get Info on a Minecraft Server}")
    async def mc_ping(self, ctx, server: str, port: int = None):
        async with ctx.typing():
            status = await self.unified_mc_ping(server, port)

            title = f"<:a:730460448339525744> {server}{(':' + str(port)) if port is not None else ''} is online."
            if status.get("online") is False:
                embed = discord.Embed(color=discord.Color.green(),
                                      title=f"<:b:730460448197050489> {server}{(':' + str(port)) if port is not None else ''} is offline.")
                await ctx.send(embed=embed)
                return

        embed = discord.Embed(color=discord.Color.green(), title=title, description=f"Version: {status.get('version')}")
        embed.add_field(name="Players Online", value=status.get("player_count"))
        ping = status.get("ping", "Not Available")
        embed.add_field(name="Latency", value=ping if ping != "None" else "Not Available")

        await ctx.send(embed=embed)
        
    @commands.command(
        brief="{Get a User's Skin}")
    @commands.cooldown(1, 2.5, commands.BucketType.user)
    @commands.guild_only()
    @commands.bot_has_permissions(use_external_emojis=True, embed_links=True)
    async def skin(self, ctx, *, gamertag: str):
        
        #Define author to make stuff shorter
        mem = ctx.author
        
        redmark = "<:redmark:738415723172462723"
      
        response = await self.ses.get(f"https://api.mojang.com/users/profiles/minecraft/{gamertag}")
        
        #If there is no player found
        if response.status == 204:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, That Player doesn't Exist", 
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
                    description=f"{redmark} __*{mem.mention}, You have to Slow Down", 
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
        
    @commands.command(
        brief="{Get a List of Name History on MC Player}", 
        aliases=['namehistory', 'namelist'])
    @commands.guild_only()
    @commands.cooldown(1, 2.5, commands.BucketType.user)
    @commands.is_owner()
    @commands.bot_has_permissions(use_external_emojis=True)
    async def names(self, ctx, gamertag: str):
      
        #Make the embed first
        e = discord.Embed(
            description="{Shown from Most `Recent` to `Oldest`}")
        
        #Define custom emoji as a var
        redmark = "<:redmark:738415723172462723>"
        
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
        
        #Store the username as a variable  
        name1 = data['username']
        
        #Store the user name history
        #As a variable
        history = data['name_history'][::-1]
        
        #Make a variable we will add on to
        #Later
        num = 0
        #Reverse all the numbers
        num_list = list(range(len(history)))[::-1]
        
        #Iterate through the list of dicts
        for item in history:
            username = item['name']
            user_date = item['changedToAt']
            #Check to make sure we don't count
            #Original name
            if item['changedToAt'] == "Original Name":
                namedate = user_date
            else:
                namedate = datetime.strptime(user_date, "%m/%d/%Y").strftime('%a/%b %d/%Y')
            
            #Make fields
            fields = [("•------------------•", 
                     f"**{num_list[num]+1}.** `{username}` - {namedate}", True)]
                     
            #Adds to the variable we stored above
            num += 1

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
            name=f"{gamertag}'s Name History", 
            icon_url=skin_head)
            
        e.set_thumbnail(
            url=f"https://minotar.net/bust/{gamertag}/100.png")
            
        #e.set_thumbnail(
            #url=f"https://minotar.net/helm/{gamertag}/75.png)")
                
        #Set footer
        e.set_footer(
            text=f"Requested by {mem}")
        e.timestamp = datetime.utcnow()
                
        #Send embed
        await ctx.send(embed=e)

    @commands.command(
        name="uuid", 
        brief="{Get a UUID with a Username}",
        usage="uuid <player>")
    @commands.cooldown(1, 2.5, commands.BucketType.user)
    @commands.guild_only()
    async def get_uuid(self, ctx, *, gamertag: str):
        
        #Get the api
        r = await self.ses.post("https://api.mojang.com/profiles/minecraft", json=[gamertag])
        
        #j[0]['id'] \/
        j = json.loads(await r.text())  
        #If a user couldn't be found
        if not j:
            await ctx.send(
                embed=discord.Embed(color=discord.Color.green(), description="That user could not be found."))
            return
        #Make the embed to send
        e = discord.Embed(
            description=f"*UUID for **{gamertag}**:* ``{j[0]['id']}``")
        
        #Make thumbnail
        #The head of the username/skin
        e.set_thumbnail(
            url=f"https://minotar.net/avatar/{gamertag}/100.png")
        
        #Send embed
        await ctx.send(embed=e)

    @commands.command(name="gamertag", brief="{Get a Gamertag with a UUID}")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def get_gamertag(self, ctx, uuid: str):
        """`Get somebody's username with their UUID`"""
        if not 30 < len(uuid) < 34:
            await ctx.send(embed=discord.Embed(color=discord.Color.green(), description="That's not a valid mc uuid!"))
            return
        response = await self.ses.get(f"https://api.mojang.com/user/profiles/{uuid}/names")
        if response.status == 204:
            await ctx.send(embed=discord.Embed(color=discord.Color.green(), description="That player doesn't exist!"))
            return
        j = json.loads(await response.text())
        name = j[len(j) - 1]["name"]
        await ctx.send(embed=discord.Embed(color=discord.Color.green(), description=f"{uuid}: ``{name}``"))

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
        usage="unenchant <enchantment_text>")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def unenchant(self, ctx, *, msg):
        lang = {}
        
        for key in list(self.g.enchantLang):
            lang[self.g.enchantLang[key]] = key
        await self.lang_convert(ctx, str(msg), lang)
        
    @command(
        brief="{Get a Random Cursed Minecraft Image}", 
        usage="cursed")
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def cursed(self, ctx):
        #Get the images from 'global.py'
        images = self.g.cursedImages
        
        e = discord.Embed(
            color=0x420000)
        e.set_image(
            url="http://olimone.ddns.net/images/cursed_minecraft/" + random.choice(images))
        
        await ctx.send(embed=e)

    @commands.command(name="mcsales", brief="{Get the Total Sales on Minecraft}")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def mc_sales(self, ctx):
        """`Shows all the sales of minecraft`"""
        r = await self.ses.post("https://api.mojang.com/orders/statistics",
                                json={"metricKeys": ["item_sold_minecraft", "prepaid_card_redeemed_minecraft"]})
        j = json.loads(await r.text())
        await ctx.send(embed=discord.Embed(color=discord.Color.dark_green(),
                                           description=f"**{j['total']}** total Minecraft copies sold, **{round(j['saleVelocityPerSeconds'], 3)}** copies sold per second."))

    @commands.command(name="randomserver", brief="{Get a Random Server}")
    async def random_mc_server(self, ctx):
        s = choice(self.g.mc_servers)
        try:
            online = MinecraftServer.lookup(s['ip'] + ":" + str(s['port'])).status()
            stat = "<:online:692764696075304960>"
        except Exception:
            stat = "<:offline:692764696431951872>"
        await ctx.send(embed=discord.Embed(color=discord.Color.green(),
                                           description=f"{stat} \uFEFF {online}``{s['ip']}:{s['port']}`` {s['version']} ({s['type']})\n{s['note']}"))

    @commands.command(name="buildidea", brief="{Get a Random Build Idea}")
    async def build_idea(self, ctx):
        """`Gives a random Minecraft Build Idea`"""
        if choice([True, False]):
            await ctx.send(embed=discord.Embed(color=discord.Color.dark_green(),
                                               description=f"{choice(self.first)} {choice(self.prenouns)}{choice(['!', ''])}"))
        else:
            await ctx.send(embed=discord.Embed(color=discord.Color.dark_green(),
                                               description=f"{choice(self.first)} a {choice(self.sizes)}, {choice(self.colors)} {choice(self.nouns)}{choice(['!', ''])}"))

    @commands.command(name="mccolorcodes", brief="{Colorcodes for Minecraft Text}")
    async def mc_color_codes(self, ctx):
        """`Gets the colorcodes for Minecraft Text`"""
        embed = discord.Embed(color=discord.Color.dark_green(),
                              description="Text in Minecraft can be formatted using different codes and\nthe section (``§``) sign.")
        embed.set_author(name="Minecraft Formatting Codes")
        embed.add_field(name="Color Codes", value="<:red:697541699706028083> **Red** ``§c``\n"
                                                  "<:yellow:697541699743776808> **Yellow** ``§e``\n"
                                                  "<:green:697541699316219967> **Green** ``§a``\n"
                                                  "<:aqua:697541699173613750> **Aqua** ``§b``\n"
                                                  "<:blue:697541699655696787> **Blue** ``§9``\n"
                                                  "<:light_purple:697541699546775612> **Light Purple** ``§d``\n"
                                                  "<:white:697541699785719838> **White** ``§f``\n"
                                                  "<:gray:697541699534061630> **Gray** ``§7``\n")
        embed.add_field(name="Color Codes", value="<:dark_red:697541699488055426> **Dark Red** ``§4``\n"
                                                  "<:gold:697541699639050382> **Gold** ``§6``\n"
                                                  "<:dark_green:697541699500769420> **Dark Green** ``§2``\n"
                                                  "<:dark_aqua:697541699475472436> **Dark Aqua** ``§3``\n"
                                                  "<:dark_blue:697541699488055437> **Dark Blue** ``§1``\n"
                                                  "<:dark_purple:697541699437592666> **Dark Purple** ``§5``\n"
                                                  "<:dark_gray:697541699471278120> **Dark Gray** ``§8``\n"
                                                  "<:black:697541699496444025> **Black** ``§0``\n")
        embed.add_field(name="Formatting Codes", value="<:bold:697541699488186419> **Bold** ``§l``\n"
                                                       "<:strikethrough:697541699768942711> ~~Strikethrough~~ ``§m``\n"
                                                       "<:underline:697541699806953583> __Underline__ ``§n``\n"
                                                       "<:italic:697541699152379995> *Italic* ``§o``\n"
                                                       "<:obfuscated:697541699769204736> ||Obfuscated|| ``§k``\n"
                                                       "<:reset:697541699697639446> Reset ``§r``\n")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Minecraft))
