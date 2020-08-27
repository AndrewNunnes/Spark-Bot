
#•----------Modules-----------•#

import discord

from discord.ext.commands import command, bot_has_permissions, has_permissions, guild_only, Cog, BadArgument, BadUnionArgument

from typing import Optional, Union

import typing

import asyncio

from datetime import datetime

#•----------Class----------•#

class Channels(Cog):
  
  """`{Channel Management}`"""
  
  def __init__(self, bot):
    self.bot = bot

#•---------Commands----------•#
  
  @command(
    brief="{Create a New Channel}", 
    usage="newtc <name> (category) (slowmode_delay[in seconds]) (reason)", 
    aliases=['createtextchannel', 'createtc'])
  @guild_only()
  @has_permissions(manage_channels=True)
  @bot_has_permissions(manage_channels=True)
  async def newtc(self, ctx, name, category: discord.CategoryChannel=None, slowmode: int=None, *, reason=None):
    
    guild = ctx.guild
    
    channel = await guild.create_text_channel(name=name, category=category, slowmode_delay=slowmode, reason=reason)
    
    await asyncio.sleep(0.5)
    
    e = discord.Embed(
      description=f"Yo {ctx.author.mention}, I just made {channel.mention} for you", 
      color=discord.Color.darker_grey())
      
    e.timestamp = datetime.datetime.utcnow()
    
    await ctx.send(embed=e)
    
    if len(name) > 25:
      await ctx.send("New name can't be longer than 25 letters")
      return
      
    else:
      if len(name) < 2:
        await ctx.send("New name must be at least 2 letters long")
        return
    
  @newtc.error
  async def newtc_error(self, ctx, error):
    if isinstance(error, BadArgument):
        e = discord.Embed(
            description='Either:\n• You need to provide a name for it\n• The Category doesn\'t exist\n• When saying names with spaces in them use this format: `"Name goes here with spaces"`\n• When saying slowmode delay, use a number bruh', 
            color=0x420000)
        
        await ctx.send(embed=e)
    else:
        raise(error)
      
  @command(
    brief="{Create a New Voice Channel}", 
    usage="newvc <name> (category) (bitrate[number]) (user_limit[number]) (reason)", 
    aliases=['createvc', 'newvoicechannel'])
  @guild_only()
  @has_permissions(manage_channels=True)
  @bot_has_permissions(manage_channels=True)
  async def newvc(self, ctx, name, category: discord.CategoryChannel=None, bitrate: int=None, user_limit: int=None, *, reason=None):
    
    guild = ctx.guild
    
    channel = await guild.create_voice_channel(
      name=name, category=category, 
      bitrate=bitrate, user_limit=user_limit, 
      reason=reason)
    
    await asyncio.sleep(0.5)
      
    e = discord.Embed(
      description=f"Yo {ctx.author.mention}, I just made {channel.mention} for you")
      
    e.timestamp = datetime.utcnow()
    
    await ctx.send(embed=e)
    
    if len(name) > 25:
      await ctx.send("New name can't be longer than 25 letters")
      return
    else:
      if len(name) < 2:
        await ctx.send("New name must be at least 2 letters long")
        return
    
  @newvc.error
  async def newvc_error(self, ctx, error):
    if isinstance(error, BadArgument):
        e = discord.Embed(
            description='Either:\n• You need to provide a name for it\n• The Category doesn\'t exist\n• When saying names with spaces in them use this format: `"Name goes here with spaces"`\n• Use numbers for the bitrate, and user limit', 
            color=0x420000)
      
        await ctx.send(embed=e)
    else:
        raise(error)
      
  @command(
    brief="{Delete a Channel}", 
    usage="delete <channel>", 
    aliases=['delchannel', 'deletech', 'deletechann', 'delchann'])
  @guild_only()
  @has_permissions(manage_channels=True)
  @bot_has_permissions(manage_channels=True)
  async def deletechannel(self, ctx, channel: Union[discord.TextChannel, discord.VoiceChannel], *, reason=None):
    
    await channel.delete(reason=reason)
    
    await asyncio.sleep(0.5)
    
    await ctx.send(f"Yo {ctx.author.mention}, I just deleted {channel} for you")

  @command(
    brief="{Get a List of Channels in the Server}", 
    usage="chlist", 
    aliases=['channellist', 'channelist'])
  @guild_only()
  async def chlist(self, ctx):
    pass

def setup(bot):
  bot.add_cog(Channels(bot))
