import discord
from discord.ext import commands
import datetime
import asyncio
import typing

class Category(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(
    brief="{Create a New Category}", 
    usage="createcategory <name> (reason)")
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def createcategory(self, ctx, *, name, overwrites=None, reason=None):
    #position: int=None, reason=None):
    
    guild = ctx.guild
    
    await guild.create_category(name=name, overwrites=overwrites, reason=reason)
    
    await asyncio.sleep(0.5)
    
    e = discord.Embed(
      description=f"Yo {ctx.author.mention}, I just made a new category for you: `{{{name}}}`", 
      color=discord.Color.darker_grey())
      
    e.timestamp = datetime.datetime.utcnow()
    
    await ctx.send(embed=e)
    
    if len(name) > 25:
      await ctx.send("New name can't be longer than 25 letters")
      
    else:
      if len(name) < 2:
        await ctx.send("New name must be at least 2 letters long")
    
  @commands.command(
    brief="{Delete a Category}", 
    usage="deletecategory <category_name/id>")
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def deletecategory(self, ctx, category: discord.CategoryChannel, *, reason=None):
    
    guild = ctx.guild
    
    category = await category.delete(reason=reason)
    
    await ctx.send(f"Yo {ctx.author.mention}, I just deleted `{{{category}}}` for you")
    
  @commands.command(
    brief="{Edit a Category}", 
    usage="editcategory <category_name/id> <name> (position) (reason)")
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def editcategory(self, ctx, category: discord.CategoryChannel, *, name=None, position: int=None, reason=None):
    
    categoryname = category.name
    category_position = category.position
    
    if position is None:
      position = category.position
      
      await category.edit(reason=reason, name=name)
        
      e = discord.Embed(
        description=f"I've changed the category `{categoryname}` from:\n__*{categoryname}*__, Position: ({category_position}) to:\n__*{name}*__, Position: ({position})", 
        color=discord.Color.darker_grey())
      
      e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
      
      e.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=e)
      
    elif name is None:
      new = category.name
      
      await category.edit(reason=reason, name=name, position=position)
      
      e = discord.Embed(
        description=f"I've changed the category `{categoryname}` from:\n__*{categoryname}*__, Position: ({category_position}) to:\n__*{name}*__, Position: ({position})", 
        color=discord.Color.darker_grey())
        
      e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
      e.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=e)
      
    #Checking if the new name
    #Is too long
    elif len(name) > 25:
        await ctx.send("Name can't be longer than 25 characters")
    
    #Checking if the new name
    #Is too short
    else:
      if len(name) < 2:
        await ctx.send("Name must be at least 2 letters long")
    
  @commands.command(
    brief="{Clone a Category/Text-Channel/Voice-Channel}", 
    usage="clone <channel/category_to_edit> (new_name) (reason)")
  @commands.guild_only()
  @commands.has_permissions(manage_channels=True)
  async def clone(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel], *, name=None, reason=None):
    
    channelname = channel.name
    
    msg = await channel.clone(name=name, reason=reason)
    
    await ctx.send(f"Yo {ctx.author.mention}, I just cloned {channelname} for you")
    
    #Checking if the new name
    #Is too long
    if len(name) > 25:
      await ctx.send("New name can't be longer than 25 letters")
    
    #Checking if the new name
    #Is too short
    else:
      if len(name) < 2:
        await ctx.send("New name must be at least 2 letters long")

def setup(bot):
  bot.add_cog(Category(bot))
