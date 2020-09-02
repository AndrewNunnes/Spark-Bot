
#•----------Modules-----------•#

import discord

from discord.ext.commands import command, bot_has_permissions, has_permissions, guild_only, Cog, \
BadArgument, BadUnionArgument, cooldown, is_owner, BucketType

from typing import Optional, Union

import asyncio

import datetime

from aiohttp import ClientSession

import io
#•----------Class----------•#

class Channels(Cog):

  """`{Channel Management}`"""
  
  def __init__(self, bot):
    self.bot = bot
    
    #Define our aiohttp clientsession
    #For easier access in other functions
    self.ses = ClientSession(loop=self.bot.loop)
    
#•----------Functions----------•#
  #Run aiohttp session
  #And close when complete
  def cog_unload(self):
      self.bot.loop.run_until_complete(self.ses.close())

#•---------Commands----------•#

  @command(
      brief="{Nuke a Channel}",
      usage="nuke (#channel)")
  @guild_only()
  @cooldown(1, 25.0, BucketType.user)
  @has_permissions(manage_channels=True)
  @bot_has_permissions(manage_channels=True)
  async def nuke(self, ctx, channel: discord.TextChannel=None):
    
      #Makes it optional to choose a channel to delete
      #Or just delete the current channel
      channel = ctx.channel if channel is None else channel
      
      #Clone the channel first  
      chan = await channel.clone(
          reason="Nuked")
      
      #url we're getting
      gif_url = "http://i-download.imgflip.com/4d4pzc.gif"
      #Get the url
      resp = await self.ses.get(gif_url)
      #If the url doesn't exist
      if resp.status != 200:
          return
        
      data = io.BytesIO(await resp.read())

      await chan.send("Nuked this channel 🤯", file=discord.File(data, gif_url))

      #Then delete the channel command was invoked in
      await channel.delete(reason="To Nuke")

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
