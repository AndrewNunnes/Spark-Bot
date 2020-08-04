import discord
from discord.ext import commands
from typing import Optional
import typing
import asyncio
import datetime

class Channels(commands.Cog):
  
  """{Channel Management}"""
  
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(
    brief="{Create a New Channel}", 
    usage="textchannel <name> (category) (slowmode_delay[in seconds]) (reason)")
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def textchannel(self, ctx, name, category: discord.CategoryChannel=None, slowmode: int=None, *, reason=None):
    
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
      
    else:
      if len(name) < 2:
        await ctx.send("New name must be at least 2 letters long")
    
  @textchannel.error
  async def textchannel_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      e = discord.Embed(
        description='Either:\n• You need to provide a name for it\n• The Category doesn\'t exist\n• When saying names with spaces in them use this format: `"Name goes here with spaces"`\n• When saying slowmode delay, use a number bruh', 
        color=0x420000)
        
      await ctx.send(embed=e)
      
  @commands.command(
    brief="{Create a New Voice Channel}", 
    usage="voicechannel <name> (category) (bitrate[number]) (user_limit[number]) (reason)")
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def voicechannel(self, ctx, name, category: discord.CategoryChannel=None, bitrate: int=None, user_limit: int=None, *, reason=None):
    
    guild = ctx.guild
    
    channel = await guild.create_voice_channel(
      name=name, category=category, 
      bitrate=bitrate, user_limit=user_limit, 
      reason=reason)
    
    await asyncio.sleep(0.5)
      
    e = discord.Embed(
      description=f"Yo {ctx.author.mention}, I just made {channel.mention} for you", 
      color=discord.Color.darker_grey())
      
    e.timestamp = datetime.datetime.utcnow()
    
    await ctx.send(embed=e)
    
    if len(name) > 25:
      await ctx.send("New name can't be longer than 25 letters")
    else:
      if len(name) < 2:
        await ctx.send("New name must be at least 2 letters long")
    
  @voicechannel.error
  async def voicechannel_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      e = discord.Embed(
        description='Either:\n• You need to provide a name for it\n• The Category doesn\'t exist\n• When saying names with spaces in them use this format: `"Name goes here with spaces"`\n• Use numbers for the bitrate, and user limit', 
        color=0x420000)
      
      await ctx.send(embed=e)
      
  @commands.command(
    brief="{Delete a Channel}", 
    usage="delete <channel>")
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def deletechannel(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel], *, reason=None):
    
    guild = ctx.guild
    
    await channel.delete(reason=reason)
    
    await asyncio.sleep(0.5)
    
    await ctx.send(f"Yo {ctx.author.mention}, I just deleted {channel} for you")
    
  @commands.command(
    brief="{Info on a Channel}", 
    usage="chinfo <#channel>")
  @commands.guild_only()
  async def chinfo(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel]):
    
    #bitrate = discord.VoiceChannel.bitrate
    
    if isinstance(channel, discord.VoiceChannel):
      
      chtype = discord.ChannelType
      
      e = discord.Embed(
        title=f"Info for {channel} `Voice Channel`",
        description=f"**>Name:** {channel.name}\n**>ID:** {channel.id}\n**>Position**: {channel.position}\n**>Bit Rate:** {channel.bitrate}\n**>User Limit:** {channel.user_limit}\n**>Members in Channel:** {len(channel.members)}\n**>Created At:** {channel.created_at}", 
        color=discord.Color.darker_grey())
        
      #await ctx.send(embed=e)
      
    elif isinstance(channel, discord.TextChannel):
      
      e = discord.Embed(
        title=f"Info for {channel} `Text Channel`", 
        description=f"**>Name:** {channel.name}\n**>ID:** {channel.id}\n**>Topic:** {channel.topic}\n**>Position:** {channel.position}\n**>Slowmode Delay:** {channel.slowmode_delay}\n**>NSFW?** {channel.is_nsfw()}\n**>News Channel?** {channel.is_news()}\n**>Under Category:** {channel.category}\n**>Created At:** {channel.created_at}", 
        color=discord.Color.darker_grey())
        
      e.set_author(
        name=f"{ctx.author}", 
        icon_url=ctx.author.avatar_url)
        
      #await ctx.send(embed=e)
        
    else:
      
      e = discord.Embed(
        description="_*• That Channel doesn't exist*_", 
        color=0x420000)
        
    await ctx.send(embed=e)
    
  @chinfo.error
  async def chinfo_error(self, ctx, error):
    if isinstance(error, commands.BadUnionArgument):
      e = discord.Embed(
        description='Either:\n• When specifying a Voice Channel, only use the name of it\nExample: `!chinfo "Voice Channel"`\n• That Channel does not exist', 
        color=0x420000)
        
      await ctx.send(embed=e)
 
  @commands.command(
    brief="{Get a List of Channels in the Server}", 
    usage="channels")
  @commands.guild_only()
  #@commands.has_permissions(manage_channels=True)
  async def channels(self, ctx):
    pass
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
def setup(bot):
  bot.add_cog(Channels(bot))
