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

    #Setup global variables for modlogs
    self.modlogs = False

    self.anti_invite = False

    self.edit_delete = False

    self.channel_log = False
    #Must all default to False

  @commands.command(
    brief="{Check Current ModLogs Status}", 
    usage="logstatus", 
    aliases=['modlogsstatus', 'logsstatus', 'modlogstatus']
  )
  @commands.guild_only()
  @commands.has_permissions(manage_guild=True)
  async def logstatus(self, ctx):

    #Variables for checking if logs are on or off
    modlogs = bool(self.modlogs)

    edit_del = bool(self.edit_delete)

    anti_inv = bool(self.anti_invite)

    #Variables to show the off or on emoji
    state1 = "<:online:728377717090680864>" if modlogs else "<:offline:728377784207933550>"

    state2 = "<:online:728377717090680864>" if edit_del else "<:offline:728377784207933550>"

    state3 = "<:online:728377717090680864>" if anti_inv else "<:offline:728377784207933550>"

    #Send and make embed
    e = discord.Embed(
      description=f"**{state1} Modlogs is {modlogs}\n{state2} Edit/Del Logs is {edit_del}\n{state3} Anti Invite is {anti_inv}**", 
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

    #Only defining for the lambda
    guild = ctx.guild

    try:
      names = ['log']
      #Checks if there's a channel 
      #containing log in the name
      channel = discord.utils.find(
        lambda channel:any(
          map(lambda c: c in channel.name, names)), 
          guild.text_channels)
        
      if not channel:

        await ctx.send("There is no Logs channel to send modlogs to")

        return

    except Exception:
      pass

    #Check if user argument is 'on' or 'off'
    if state is True:

      self.modlogs = True

      await ctx.send('<:online:728377717090680864> Log system has been turned on')
    else:
      if state is False:
        #Making all other options False
        self.modlogs = False
        self.edit_delete = False
        self.anti_invite = False
        self.channel_log = False

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

    #Check if message is 'off'
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

    #Check to see if modlogs are off
    if self.anti_invite==False or self.modlogs==False:
      return

    elif self.anti_invite==True:
    
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
            await message.channel.send("Can't find a Logs Channel")
        except Exception:
          pass
            
            #guild = message.guild
            
            #ow = {
              #guild.default_role: discord.PermissionOverwrite(read_messages=False)
            #}
            #for role in guild.roles:
              #if role.permissions.view_audit_log:
                #ow[role] = discord.PermissionOverwrite(read_messages=True)
            
            #await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")

          #await channel.send(embed=e)

  #Listen for when a channel
  #Is created
  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):

    #Check if modlogs are off
    if self.channel_log==False or self.modlogs==False:
      return

    #Check if modlogs are on
    elif self.channel_log==True:
      pass

  #Send an edited message to 
  #A logs channel
  @commands.Cog.listener()
  async def on_message_edit(self, before, after):

    #Check to see if modlogs are off
    if self.edit_delete==False or self.modlogs==False:
      return

    #Check if modlogs are on
    elif self.edit_delete==True:

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

      #Make embed
      e = discord.Embed(
        description=f'**Message Sent by {after.author.mention} Edited In {after.channel.mention}** [Jump to Message]({after.jump_url})', 
        color=discord.Color.dark_blue()
      )

      #Setup fields
      fields = [("**Before:**", before.content, False), 
                ("**After:**", after.content, False)]
      
      for name, value, inline in fields:
        e.add_field(
          name=name, 
          value=value, 
          inline=inline
        )

      e.timestamp = datetime.datetime.utcnow()

      e.set_footer(
        text=f'{before.author}', 
        icon_url=f'{before.author.avatar_url}')

      await channel.send(embed=e)

      #IF channel doesn't exist
      if not channel:
        pass
        #ow = {
          #guild.default_role: discord.PermissionOverwrite(read_messages=False)}
          
        #for role in guild.roles:
          #if role.permissions.view_audit_log:
            #ow[role] = discord.PermissionOverwrite(read_messages=True)
            
        #await guild.create_text_channel("⚠️ Server Logs", overwrites=ow, reason="Logging for Moderation")

  #Sends a deleted message 
  #To logs channel
  @commands.Cog.listener()
  async def on_message_delete(self, message):

    #Check if modlogs are off
    if self.modlogs==False or self.edit_delete==False:
      return

    #Check if modlogs are on
    elif self.edit_delete==True:

        #Makes sure not to count embeds
        if message.embeds:
          return

        #Makes sure not to count
        #Bot messages
        if message.author.bot:
          return

        guild = message.guild

        #Check if there's a 
        #Logs channel
        names = ['log']
        channel = discord.utils.find(
          lambda channel:any(
            map(lambda c: c in channel.name, names)), 
            guild.text_channels)

        #Make embed
        e = discord.Embed(
          description=f'**Message Sent By {message.author.mention} Deleted In {message.channel.mention}**', 
          color=discord.Color.dark_red()
        )

        e.timestamp = datetime.datetime.utcnow()

        e.add_field(
          name="**Message:**", 
          value=message.content, 
          inline=False
        )

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
