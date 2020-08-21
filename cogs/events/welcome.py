import discord
from discord.ext import commands
import datetime
import asyncio
import aiosqlite

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #Sends a fancy embed to show the prefixes    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
      names = ['comman', 'bot']
      channel = discord.utils.find(
        lambda channel:any(
          map(lambda w: w in channel.name, names)),
        guild.text_channels) #When the bot joins a server, this will check for a bot commands channel to send an embed
        
      if not channel: #If a bot commands channel doesn't exist, it'll look for a general channel
        newchann = ['gener', 'chat', 'welc', 'memb']
        new = discord.utils.find(
          lambda new:any(
            map(lambda n: n in new.name, newchann)),
            guild.text_channels)
            
        embed = discord.Embed(
          color=discord.Color.darker_grey(), 
          description=f"What's up everyone! Type in `!help` to see all of my available commands and get started!\n\n")
          
        embed.timestamp = datetime.datetime.utcnow()
        await new.send(embed=embed)
            
      embed = discord.Embed(color=discord.Color.darker_grey(),
      description=f"What's up everyone! Type `!help` to see all of my commands and get started!\n\n")
      
      embed.timestamp = datetime.datetime.utcnow()
      await channel.send(embed=embed)
      
      #await guild.create_custom_emoji()
    
    #Welcoming new Members
    @commands.Cog.listener()
    async def on_member_join(self, member):

      conn = await aiosqlite.connect("main.db")
      
      cursor = await conn.cursor()

      await cursor.execute(f"SELECT channel_id FROM welcome WHERE guild_id = {member.guild.id}")

      result = cursor.fetchone()

      if result is None:
        return

      else:

        cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {member.guild.id}")
        result1 = cursor.fetchone()

        #List of optionaal variables
        #For the welcome message
        members = len(list(member.guild.members))

        mention = member.mention

        user = member.name

        guild = member.guild

        gicon = member.guild.icon_url

        micon = member.avatar_url

        #Adjust the embed to what the user 
        #Set the variables to
        e = discord.Embed(
          colour=discord.Colour.dark_green(), 
          description=str(result[0]).format(members=members, mention=mention, user=user, guild=guild))

        e.set_thumbnail(url=f"{member.avatar_url}")

        e.set_author(name=f"Welcome {member.name} to {member.guild}", icon_url=f"{member.avatar_url}")

        e.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")

        e.timestamp = datetime.datetime.utcnow()

        #Get the channel the user set 
        #To send this welcome message to
        channel = self.bot.get_channel(id=int(result[0]))

        await channel.send(embed=e)

        #IF there is no message set
        if not result1:
          #Adjust the embed to what the user 
          #Set the variables to
          e = discord.Embed(
            colour=discord.Colour.dark_green(), description=f"What's up {member}, and welcome to the server! You are now member {len(list(member.guild.members))}")

          e.set_thumbnail(url=f"{member.avatar_url}")

          e.set_author(name=f"Welcome {member.name} to {member.guild}", icon_url=f"{member.avatar_url}")

          e.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")

          e.timestamp = datetime.datetime.utcnow()

          #Get the channel the user set 
          #To send this welcome message to
          channel = self.bot.get_channel(id=int(result[0]))

          await channel.send(embed=e)
      
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def welcome(self, ctx):

      e = discord.Embed(
        title="Available Setup Commands", 
        color=discord.Color.darker_grey()
      )

      e.add_field(
        name="_*welcome channel {Set the channel to send Welcome Messages to}*_", 
        value="{{`{ctx.prefix}welcome channel <#channel>`}}", 
        inline=True)

      e.add_field(
        name="_*welcome text {Set the channel to send Welcome Messages to}*_", 
        value="{{`{ctx.prefix}welcome text <text>`}}", 
        inline=True)

      await ctx.send(embed=e)

    @welcome.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def channel(self, ctx, channel: discord.TextChannel):

      conn = await aiosqlite.connect("main.db")
      
      cursor = await conn.cursor()

      await cursor.execute(f"SELECT channel_id FROM welcome WHERE guild_id = {ctx.guild.id}")

      result = cursor.fetchone()

      if result is None:

        chann = ("INSERT INTO welcome(guild_id, channel_id) VALUES(?, ?)", ctx.guild.id, channel.id)
        await ctx.send(f"Channel has been set to {channel.mention}")

      elif result is not None:

        chann = ("UPDATE welcome SET channel_id = ? WHERE guild_id = ?", channel.id, ctx.guild.id)
        await ctx.send(f"Channel has been updated to {channel.mention}")

      await cursor.execute(chann)

      await conn.commit()

      await cursor.close()

      await conn.close()

    @welcome.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def text(self, ctx, *, text):

      #Connect to the database
      conn = await aiosqlite.connect("main.db")
      
      #Define the database cursor
      cursor = await conn.cursor()

      #Get the text query from welcome table
      await cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {ctx.guild.id}")

      result = cursor.fetchone()

      #IF there is no result
      if result is None:

        msg = ("INSERT INTO welcome(guild_id, msg) VALUES(?, ?)", ctx.guild.id, text)

        e = discord.Embed(
          title="**Welcome Message Set", 
          description=f"**New Message:** {text}", 
          color=discord.Color.dark_green()
        )

        e.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=e)

      #IF there is a result
      elif result is not None:

        msg = ("UPDATE welcome SET text = ? WHERE guild_id = ?", text, ctx.guild.id)

        e = discord.Embed(
          title="**Welcome Message Updated", 
          description=f"**New Message:** {text}", 
          color=discord.Color.dark_green()
        )

        e.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=e)

      #Execute to the cursor
      await cursor.execute(msg)

      #Commit (Save) to the database
      await conn.commit()

      #Close the cursor connection
      await cursor.close()

      #Close the database connection
      await conn.close()


    #Saying goodbye to leaving members
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(colour=discord.Colour.dark_red(), description=f"{member} just left the server. Thanks for visiting! Member Count: {len(list(member.guild.members))}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"Goodbye {member.name}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        channelnames = ['memb', 'new', 'user', 'User', 'gateway', 'gate', 'entrance', 'enter', 'leave']
        channel = discord.utils.find(
            lambda channel:any(
                map(lambda c: c in channel.name, channelnames)), member.guild.text_channels)
        
        if not channel:
          newlist = ['gener', 'chat', 'welc']
          newchann = discord.utils.find(
              lambda newchann:any(
                  map(lambda n: n in newchann.name, newlist)), member.guild.text_channels)
          await newchann.send("Welcome and Goodbye messages to new users won't be sent without the channel including a keyword `new`, `memb` or `user`") #In case the channel doesn't exist to welcome new people, this will find a different general or chat channel to send the error to
        message = await channel.send(embed=embed)
        await message.add_reaction("ðŸ‘‹ðŸ½")

def setup(bot):
    bot.add_cog(Welcome(bot))
