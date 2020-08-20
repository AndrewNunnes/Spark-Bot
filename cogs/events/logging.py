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

    self.modlogs = False

    self.anti_invite = False

    self.edit_delete = False

  @commands.command(
    brief="{Check Current ModLogs Status}", 
    usage="logstatus", 
    aliases=['modlogsstatus']
  )
  @commands.guild_only()
  @commands.has_permissions(manage_guild=True)
  async def logstatus(self, ctx):

    OffEdit_Delete = f"<:offline:728377784207933550> Edit/Deleted Messages Logs are {bool(self.edit_delete)}"

    OffAnti_Invite = f"<:offline:728377784207933550> AntiInvite Messages are {bool(self.anti_invite)}"

    OffModLogs = f"<:offline:728377784207933550> ModLogs are {bool(self.modlogs)}"

    OnEdit_Delete = f"<:online:728377717090680864> Edit/Deleted Messages Logs are {bool(self.edit_delete)}"

    OnAnti_Invite = f"<:online:728377717090680864> AntiInvite Messages are {bool(self.anti_invite)}"

    if self.edit_delete == True:
      OnEdit_Delete = f"<:online:728377717090680864> Edit/Deleted Messages Logs Is On"
    else:
      if self.edit_delete == False:
        OffEdit_Delete = f"<:offline:728377784207933550> Edit/Deleted Messages Logs Is Off"

    OnModLogs = f"<:online:728377717090680864> ModLogs are {bool(self.modlogs)}"

    if self.modlogs == False:
      e = discord.Embed(
        description=f"**{OffModLogs}\n{OffEdit_Delete}\n{OffAnti_Invite}**", 
        color=0x420000
      )

      e.timestamp = datetime.datetime.utcnow()

      await ctx.send(embed=e)
    else:
      if self.modlogs == True:
        e = discord.Embed(
          description=f"{OnModLogs}\n{OnEdit_Delete}\n{OnAnti_Invite}", 
          color=0x420000
        )

        e.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=e)

  @commands.command(
    brief='{Turn on/off Server Logs}', 
    usage='logs <on/off>', 
    aliases=['modlogs', 'serverlogs']
  )
  @commands.has_permissions(manage_guild=True)
  @commands.guild_only()
  async def logs(self, ctx, state: bool):

    #Check if user argument is 'on' or 'off'
    if state is True:
      self.modlogs = True

      #Create the server logs channel
      #guild = ctx.guild
      
      #ow = {
        #guild.default_role: discord.PermissionOverwrite(read_messages=False)
        #}
      #for role in guild.roles:
        #if role.permissions.view_audit_log:
          #ow[role] = discord.PermissionOverwrite(read_messages=True)
            
          #await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")

      await ctx.send('<:online:728377717090680864> Log system has been turned on')
    else:
      if state is False:
        #Making all other options False
        self.modlogs = False
        self.edit_delete = False
        self.anti_invite = False

        await ctx.send('<:offline:728377784207933550> Log system has been turned off')

  @commands.command(
    brief='{Turn on/off Logs for Messages Deleted/Edited}', 
    usage='logs <on/off>', 
    aliases=['edit_delete', 'edit/delete']
  )
  @commands.has_permissions(manage_guild=True)
  @commands.guild_only()
  async def editdel(self, ctx, state: bool):

    #Check if message is 'on'
    if state is True:
      self.edit_delete = True
      await ctx.send('<:online:728377717090680864> Logs for Messages Deleted/Edited has been turned on')
    else:
      if state is False:
        self.edit_delete = False
        await ctx.send('<:offline:728377784207933550> Logs for Messages Deleted/Edited has been turned off')

  @commands.command(
    brief='{Turn on/off Anti Invite}', 
    usage='antiinvite <on/off>', 
    aliases=['antiinv', 'anti_inv', 'anti_invite']
  )
  @commands.guild_only()
  @commands.has_permissions(manage_guild=True)
  async def antiinvite(self, ctx, state: bool):
    
    #Check if message is 'on' or 'off'
    if state is True:
      self.anti_invite = True
      await ctx.send('<:online:728377717090680864> Anti Invite has been turned on')
    else:
      if state is False:
        self.anti_invite = False
        await ctx.send('<:offline:728377784207933550> Anti Invite has been turned off')
    
  @commands.Cog.listener()
  async def on_message(self, message):

    if self.anti_invite or self.modlogs == True:
    
      #Check if a user
      #send a Discord Invite
      if "discord.gg" in message.content:
        guild = message.guild
        
        await message.delete()
        
        e = discord.Embed(
          description=f"**{message.author.mention}*__ you're not supposed to share Server Invites**", 
          color=0x420000)
        
        e.set_thumbnail(url=message.author.avatar_url)

        e.set_footer(text=f"{message.author.name} Tried to Post an Invite")

        e.timestamp = datetime.datetime.utcnow()
        
        await message.channel.send(embed=e)
        
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
            await message.channel.send("Can't find a Logs Channel ")
            
            #guild = message.guild
            
            #ow = {
              #guild.default_role: discord.PermissionOverwrite(read_messages=False)
            #}
            #for role in guild.roles:
              #if role.permissions.view_audit_log:
                #ow[role] = discord.PermissionOverwrite(read_messages=True)
            
            #await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")

          #await channel.send(embed=e)
        except commands.BotMissingPermissions:
          await message.channel.send("Seems like I'm missing permissions to make a Modlogs Channel")

    else:
      pass

  #Send an edited message to 
  #A logs channel
  @commands.Cog.listener()
  async def on_message_edit(self, before, after):

    if self.edit_delete or self.modlogs == True:

      #Makes sure not to count embeds
      if before.embeds or after.embeds:
        return

      #Check if message edited
      #Is by a bot
      if before.author.bot:
        return

      guild = before.guild
      
      #Check if there's a 
      #Logs channel
      names = ['log']
      channel = discord.utils.find(
        lambda channel:any(
          map(lambda c: c in channel.name, names)), 
          guild.text_channels)

      e = discord.Embed(
        description=f'**Message Edited by {after.author.mention} In {after.channel.mention}**\n\n**Before:** {before.content}\n\n**After:** {after.content}', 
        color=discord.Color.dark_blue()
      )

      e.timestamp = datetime.datetime.utcnow()

      e.set_footer(
        text=f'{before.author}', 
        icon_url=f'{before.author.avatar_url}')

      await channel.send(embed=e)

      if not channel:
        pass
        #ow = {
          #guild.default_role: discord.PermissionOverwrite(read_messages=False)}
          
        #for role in guild.roles:
          #if role.permissions.view_audit_log:
            #ow[role] = discord.PermissionOverwrite(read_messages=True)
            
        #await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")
    else:
      pass

  #Sends a deleted message 
  #To logs channel
  @commands.Cog.listener()
  async def on_message_delete(self, message):

    if self.modlogs or self.edit_delete == True:

        if message.embeds:
          return

        guild = message.guild

        #Check if there's a 
        #Logs channel
        names = ['log']
        channel = discord.utils.find(
          lambda channel:any(
            map(lambda c: c in channel.name, names)), 
            guild.text_channels)

        e = discord.Embed(
          description=f'**Message Deleted By {message.author.mention} In {message.channel.mention}**\n\n**Message:** {message.content}', 
          color=discord.Color.dark_red()
        )

        e.timestamp = datetime.datetime.utcnow()

        e.set_footer(
          text=f'{message.author}', 
          icon_url=f'{message.author.avatar_url}'
        )

        await channel.send(embed=e)

        if not channel:
          pass
          #ow = {
            #guild.default_role: discord.PermissionOverwrite(read_messages=False)}
            
          #for role in guild.roles:
            #if role.permissions.view_audit_log:
              #ow[role] = discord.PermissionOverwrite(read_messages=True)
              
          #await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")
    else:
      pass

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
