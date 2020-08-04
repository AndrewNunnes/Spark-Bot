import discord
from discord.ext import commands
from typing import Optional

class Channels(commands.Cog):
  
  """{Channel Management}"""
  
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(
    brief="{Create a New Channel}", 
    usage="textchannel <name> (category) (slowmode_delay[in seconds]) (reason)")
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def textchannel(self, ctx, name, *, category: discord.CategoryChannel=None, slowmode: int=None, reason=None):
    
    guild = ctx.guild
    
    channel = await guild.create_text_channel(name=name, category=category, slowmode_delay=slowmode, reason=reason)
    
    await asyncio.sleep(0.5)
    
    e = discord.Embed(
      description=f"Yo {ctx.author.mention}, I just made {channel.mention} for you", 
      color=discord.Color.darker_grey())
      
    e.timestamp = datetime.datetime.utcnow()
    
    await ctx.send(embed=e)
    
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
  async def voicechannel(self, ctx, name, *, category: discord.CategoryChannel=None, bitrate: int=None, user_limit: int=None, reason=None):
    
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
  async def deletechannel(self, ctx):
    pass
 
  @commands.command(
    brief="{Get a List of Channels in the Server}", 
    usage="channels")
  @commands.guild_only()
  #@commands.has_permissions(manage_channels=True)
  async def channels(self, ctx):
    pass
  
def setup(bot):
  bot.add_cog(Channels(bot))
