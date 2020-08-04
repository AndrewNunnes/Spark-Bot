import discord
from discord.ext import commands
import datetime
import asyncio
import re

class Logging(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_message(self, message):
    
    #Check if a user
    #send a Discord Invite
    if "discord.gg" in message.content:
      guild = message.guild
      member = message.author
      
      await message.delete()
      
      bruh = discord.Embed(
        title=f"__*{message.author.mention}*__ you're not supposed to share Server Invites", 
        color=0x420000)
      
      bruh.set_thumbnail(url=message.author.avatar_url)
      bruh.set_footer(text=f"{message.author.name.discriminator} Tried to Post an Invite")
      bruh.timestamp = datetime.datetime.utcnow()
      
      await message.channel.send(embed=bruh)
      
      names = ['log']
      #Checks if there's a channel 
      #containing log in the name
      channel = discord.utils.find(
        lambda channel:any(
          map(lambda c: c in channel.name, names)), 
          guild.text_channels)
      
      e = discord.Embed(
        title="__*Invite Attempt*__", 
        description=f"_**{message.author.name.discriminator} Tried to post an invite to a Discord Server\nShould let him know not to do it next time**_", 
        color=0x380000)
      
      e.set_thumbnail(url=message.author.avatar_url)
      e.set_footer(text=f"{message.author}")
      e.timestamp = datetime.datetime.utcnow()
      
      await channel.send(embed=e)
      
      #If a log channel doesn't exist
      #This will send
      if not channel:
        await message.channel.send("Looks like you don't have a Logs channel\n\nMaking one now...")
        
        guild = message.guild
        
        ow = {
          guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        for role in guild.roles:
          if role.permissions.kick_members:
            ow[role] = discord.PermissionOverwrite(read_messages=True)
        
        await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")

    await self.bot.process_commands(message)

def setup(bot):
  bot.add_cog(Logging(bot))
