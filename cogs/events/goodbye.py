import discord
from discord.ext import commands
import datetime
import aiosqlite

class Goodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def goodbye(self, ctx):

      e = discord.Embed(
        title="Available Setup Commands", 
        color=discord.Color.darker_grey()
      )

      e.add_field(
        name="**goodbye channel {Set the channel to send Goodbye Messages to}**", 
        value=f"{{`{ctx.prefix}goodbye channel <#channel>`}}", 
        inline=True)

      e.add_field(
        name="**goodbye text {Set the text to send Goodbye Messages to}**", 
        value=f"{{`{ctx.prefix}goodbye text <text>`}}", 
        inline=True)

      await ctx.send(embed=e)

    @goodbye.command(
      brief="{Change the Channel to Send Goodbye Messages To", 
      usage="goodbye channel <#channel>"
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def channel(self, ctx, channel: discord.TextChannel):

      conn = await aiosqlite.connect("main.db")
      
      cursor = await conn.cursor()

      await cursor.execute(f"SELECT channel_id FROM goodbye WHERE guild_id = {ctx.guild.id}")

      result = cursor.fetchone()

      if result is None:

        chann = ("INSERT INTO goodbye(guild_id, channel_id) VALUES(?, ?)")
        values = ctx.guild.id, channel.id

        await ctx.send(f"Channel has been set to {channel.mention}")

      elif result is not None:

        chann = "UPDATE goodbye SET channel_id = ? WHERE guild_id = ?"
        values = (channel.id, ctx.guild.id)

        await ctx.send(f"Channel has been updated to {channel.mention}")

      await cursor.execute(chann, values)

      await conn.commit()

      await cursor.close()

      await conn.close()

    @goodbye.command(
      brief="{Change the Goodbye Message}", 
      usage="goodbye text <new_text_here>"
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def text(self, ctx, *, text):

      #Connect to the database
      conn = await aiosqlite.connect("main.db")
      
      #Define the database cursor
      cursor = await conn.cursor()

      #Get the text query from welcome table
      await cursor.execute(f"SELECT msg FROM goodbye WHERE guild_id = {ctx.guild.id}")

      result = cursor.fetchone()

      #IF there is no result
      if result is None:

        msg = "INSERT INTO goodbye(guild_id, msg) VALUES(?, ?)"
        values = (ctx.guild.id, text)

        e = discord.Embed(
          title="**Welcome Message Set", 
          description=f"**New Message:** {text}", 
          color=discord.Color.dark_green()
        )

        e.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=e)

      #IF there is a result
      elif result is not None:

        msg = "UPDATE goodbye SET text = ? WHERE guild_id = ?"
        values = (text, ctx.guild.id)

        e = discord.Embed(
          title="**Welcome Message Updated", 
          description=f"**New Message:** {text}", 
          color=discord.Color.dark_green()
        )

        e.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=e)

      #Execute to the cursor
      await cursor.execute(msg, values)

      #Commit (Save) to the database
      await conn.commit()

      #Close the cursor connection
      await cursor.close()

      #Close the database connection
      await conn.close()
    #Saying goodbye to leaving members
    @commands.Cog.listener()
    async def on_member_remove(self, member):

      #Connect to database
      conn = await aiosqlite.connect("main.db")
      
      cursor = await conn.cursor()

      #Select queries from goodbye table
      await cursor.execute(f"SELECT channel_id FROM goodbye WHERE guild_id = {member.guild.id}")

      result = cursor.fetchone()

      #Get the channel the user set 
      #To send this welcome message to
      channel = self.bot.get_channel(id=int(result[0]))

      #Check if the channel exists 
      #In the database
      if channel is None:
        return

      #Check if there's any channels
      #In the database
      if result is None:
        return

      else:

        cursor.execute(f"SELECT msg FROM goodbye WHERE guild_id = {member.guild.id}")
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
          description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild))

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
            colour=discord.Colour.dark_green(), 
            description=f"What's up {member}, and welcome to the server! You are now member {len(list(member.guild.members))}")

          e.set_thumbnail(url=f"{member.avatar_url}")

          e.set_author(
              name=f"Welcome {member.name} to {member.guild}", 
              icon_url=f"{member.avatar_url}")

          e.set_footer(
              text=f"{member.guild}", 
              icon_url=f"{member.guild.icon_url}")

          e.timestamp = datetime.datetime.utcnow()

          await channel.send(embed=e)

def setup(bot):
    bot.add_cog(Goodbye(bot))
