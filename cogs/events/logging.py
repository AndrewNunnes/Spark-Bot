import discord
from discord.ext import commands
import datetime
import asyncio
import typing
from typing import Union
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
      
      await message.delete()
      
      bruh = discord.Embed(
        title=f"__*{message.author.mention}*__ you're not supposed to share Server Invites", 
        color=0x420000)
      
      bruh.set_thumbnail(url=message.author.avatar_url)
      bruh.set_footer(text=f"{message.author.name} Tried to Post an Invite")
      bruh.timestamp = datetime.datetime.utcnow()
      
      await message.channel.send(embed=bruh)
      
      await asyncio.sleep(1)
      
      try:
        names = ['log']
        #Checks if there's a channel 
        #containing log in the name
        channel = discord.utils.find(
          lambda channel:any(
            map(lambda c: c in channel.name, names)), 
            guild.text_channels) 
        
        e = discord.Embed(
          title="__*Invite Attempt*__", 
          description=f"_**{message.author.name} Tried to post an invite to a Discord Server\nShould let him know not to do it next time**_", 
          color=0x380000)
        
        e.set_thumbnail(url=message.author.avatar_url)
        e.set_footer(text=f"{message.author}")
        e.timestamp = datetime.datetime.utcnow()
        
        
        #If a log channel doesn't exist
        #This will send
        if not channel:
          await message.channel.send("Looks like you don't have a Logs channel\n\nMaking one now...")
          
          guild = message.guild
          
          ow = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
          }
          for role in guild.roles:
            if role.permissions.view_audit_log:
              ow[role] = discord.PermissionOverwrite(read_messages=True)
          
          await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")

        await channel.send(embed=e)
      except commands.BotMissingPermissions:
        await message.channel.send("Seems like I'm missing permissions to make a Modlogs Channel")

  #Send an edited message to 
  #A logs channel
  @commands.Cog.listener()
  async def on_message_edit(self, before, after):

    guild = before.guild
    
    #Check if there's a 
    #Logs channel
    names = ['log']
    channel = discord.utils.find(
      lambda channel:any(
        map(lambda c: c in channel.name, names)), 
        guild.text_channels)

    e = discord.Embed(
      title=f"Message Edited by {before.author}", 
      description=f'\n__*Before:*__ {before.content}\n\n__*After:*__ {after.content}\n\n__*In:*__ {message.channel.mention}', 
      color=0x2b3292
    )

    e.timestamp = datetime.datetime.utcnow()

    e.set_footer(
      text=f'{before.author}', 
      icon_url=f'{before.author.avatar_url}')

    await channel.send(embed=e)

    if not channel:
      ow = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)}
        
      for role in guild.roles:
        if role.permissions.view_audit_log:
          ow[role] = discord.PermissionOverwrite(read_messages=True)
          
      await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")

  #Sends a deleted message 
  #To logs channel
  @commands.Cog.listener()
  async def on_message_delete(self, message):

    guild = message.guild

    #Check if there's a 
    #Logs channel
    names = ['log']
    channel = discord.utils.find(
      lambda channel:any(
        map(lambda c: c in channel.name, names)), 
        guild.text_channels)

    e = discord.Embed(
      title=f'Message deleted by {message.author}', 
      description=f'__*Message Deleted:*__ {message.content}\n\n__*In:*__ {message.channel.mention}', 
      color=0x2b3292
    )

    e.timestamp = datetime.datetime.utcnow()

    e.set_footer(
      text=f'{message.author}', 
      icon_url=f'{message.author.avatar_url}'
    )

    await channel.send(embed=e)

    if not channel:
      ow = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)}
        
      for role in guild.roles:
        if role.permissions.view_audit_log:
          ow[role] = discord.PermissionOverwrite(read_messages=True)
          
      await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")

  @commands.Cog.listener()
  async def on_member_ban(self, guild, user):

  #async for entry in guild.audit_logs(action=discord.AuditLogAction.ban):
    #banned = '{0.user} banned {0.target}'.format(entry)

    channel_names = ['log']

    #Checks for a logs channel
    #To send the embeds to
    channel = discord.utils.find(
      lambda channel:any(
        map(lambda w: w in channel.name, channel_names)),
        guild.text_channels) 
      
    if not channel: 
      #If a logs channel doesn't exist
      # it'll look for a general channel
      newchann = ['gener', 'chat', 'welc', 'memb']

      new = discord.utils.find(
        lambda new:any(
          map(lambda n: n in new.name, newchann)),
          guild.text_channels)
          
      e = discord.Embed(
        color=discord.Color.darker_grey())

      fields = [
        f"__*{user.name} has been Banned {{!}}*__"]

      for name, value in fields:
        e.add_field(
          name=name, 
          value=value
        )

      e.timestamp = datetime.datetime.utcnow()
      
      await new.send(embed=e)
          
    embed = discord.Embed(color=discord.Color.darker_grey())

    fields = [
      f"__*{user.name} has been Banned {{!}}*__", 
      f'Banned by: {ctx.author}\nReason: {reason}']

    for name, value in fields:
      e.add_field(
        name=name, 
        value=value
      )
    
    embed.timestamp = datetime.datetime.utcnow()

    await channel.send(embed=embed)

def setup(bot):
  bot.add_cog(Logging(bot))
