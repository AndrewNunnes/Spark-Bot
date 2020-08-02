import discord
from discord.ext import commands
import asyncio
import datetime
import typing
from typing import Union

class Role(commands.Cog, name="__*Role Management*__"):
  def __init__(self, bot):
    self.bot = bot
    
  #Checks if the bot has all the permissions required
  def bot_perms():
    async def predicate(ctx):
      return ctx.guild is not None \
      and ctx.me.guild_permissions.all() \
      and ctx.me.guild_permissions.all_channel() \
      and ctx.me.guild_permissions.general() \
      and ctx.me.guild_permissions.text() \
      and ctx.me.guild_permissions.voice()
    return commands.check(predicate)
    
  @commands.command(brief="{Menu for Role Management}")
  @commands.guild_only()
  async def role(self, ctx):
    

    cog = self.bot.get_cog('__*Role Management*__')
    commands = cog.get_commands()

    command_desc = [f"_*{c.name}*_ - `{c.brief}`" for c in cog.walk_commands()]
    
    embed = discord.Embed(
      title=f"{cog.qualified_name}", 
      description="_*() - Optional\n<> - Required*_", 
      color=discord.Color.darker_grey())
      
    embed.add_field(
      name='_*Your Available Commands*_', 
      value="\n".join(command_desc))
    embed.timestamp = datetime.datetime.utcnow()
    
    await ctx.send(embed=embed)
    
  @commands.command(name="roleposition", brief="{Change the Position of a Role}") #usage="{Change the position of a Role}")
  @commands.guild_only()
  @bot_perms()
  @commands.has_permissions(manage_roles=True)
  async def position(self, ctx, role: discord.Role, *, position: int):
    pass
    
  @commands.command(name="rolename", brief="{Change the Name of a Role}")#description="{Change the name of a Role}")
  @commands.guild_only()
  @commands.has_permissions(manage_roles=True)
  @bot_perms()
  async def name(self, ctx, role: discord.Role, *, text):
    
    rolename = role.name
    
    await role.edit(name=text)
    
    embed = discord.Embed(
      color=discord.Color.darker_grey(), 
      description=f"Successfully changed {rolename} to {text}")
    embed.timestamp = datetime.datetime.utcnow()
    
    await ctx.send(embed=embed)
    
  @name.error
  async def name_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      
      embed = discord.Embed(
        color=discord.Color.dark_red(), 
        description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role name"``\n• Valid Syntax: `{ctx.prefix}role color <color> <role_name>`')
      embed.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=embed)
      
  @commands.command(name="rolecolor", brief="{Change the color of a Role}")
  @commands.guild_only()
  @commands.has_permissions(manage_roles=True)
  @bot_perms()
  async def color(self, ctx, color: discord.Color, *, role: discord.Role):
    rolecolor = role.color
    rolemention = role.mention
    
    await role.edit(color=color)
    
    embed = discord.Embed(
      color=discord.Color.darker_grey(), 
      description=f"Successfully changed colors for {rolemention}{{`{rolecolor}`}} to {{`{color}`}}")
      
    embed.timestamp = datetime.datetime.utcnow()
      
    await ctx.send(embed=embed)
   # await ctx.send(f"{role.mention} successfully changed colors from {role.color} to {color}")
   
  @color.error
  async def color_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      
      embed = discord.Embed(
        color=discord.Color.dark_red(), 
        description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role_name>"`\n• Valid Syntax: `{ctx.prefix}role color <color> <role_name>`')
      embed.timestamp = datetime.datetime.utcnow()
      await ctx.send(embed=embed)
    
  @commands.command(name="addrole", brief="{Add a Role to a Member}")
  @commands.guild_only()
  @bot_perms()
  @commands.has_permissions(manage_roles=True)
  async def add(self, ctx, member: discord.Member, *, role: discord.Role):
    """
    Add a Role to a User
    """
    await member.add_roles(role)
    await ctx.send(f"Successfully gave {role.mention} to: `{member.display_name}`")
    
  @add.error
  async def add_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      embed = discord.Embed(
        color=discord.Color.dark_red(), 
        description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"role_name"`\n• Valid Syntax: `{ctx.prefix}role add <member> <role_name>`')
      embed.timestamp = datetime.datetime.utcnow()
      
  @commands.command(name="removerole", brief="{Remove a Role from a Member}")
  @bot_perms()
  @commands.guild_only()
  @commands.has_permissions(manage_roles=True)
  async def remove(self, ctx, member: discord.Member, *, role: discord.Role):
      """
      Removes a role from a user
      """
      await member.remove_roles(role)
      await ctx.send(f"Successfully removed {role.mention} from: `{member.display_name}`")
      
  @remove.error
  async def remove_error(self, ctx, error):
      if isinstance(error, commands.BadArgument):
        
        e = discord.Embed(
          color=discord.Color.dark_red(), 
          description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role_name>"`\n• Valid Syntax: `{ctx.prefix}role remove <member> <role_name>`')
        e.timestamp = datetime.datetime.utcnow()
        
        await ctx.send(embed=e)
          
  #@commands.command()
  #@commands.guild_only()
  #async def rolelist(self, ctx):
    #guild = ctx.guild
    
    #rolelist = [f'']
    #embed = discord.Embed(
      #title="__*All Roles in this Server*__", 
      #description=f"{list(guild.roles)}", 
      #color=discord.Color.darker_grey())
      
    #await ctx.send(embed=embed)
          
  @commands.command(name="roleinfo", brief="{Get Info on a Role}")
  @commands.guild_only()
  @bot_perms()
  async def info(self, ctx, *, role: discord.Role):
      """
      Pulls info about a role
      """
      embed = discord.Embed(
          title=f"Info on {role.mention}", 
          description=f"**>Role ID:** {role.id}\n**>Server it belongs to:** {ctx.guild}\n**>Does it Display from others?:** {role.hoist}\n**>Position:** {role.position}\n**>Created at:** {role.created_at.strftime('%d/%m/%Y')}", 
          color=discord.Color.darker_grey())
      embed.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=embed)
      
  @info.error
  async def info_error(self, ctx, error):
      if isinstance(error, commands.BadArgument):
          await ctx.send("That isn't a valid role")
          
  @commands.command(name="rolelist", brief="{Get a List of All the Roles in the Server}")
  @commands.guild_only()
  @bot_perms()
  async def _list(self, ctx):
    """
    List of Roles in the Server
    """
    guild = ctx.guild
    
    rolelist = [role.mention for role in guild.roles] # List of the names for the roles in the guild
    
    embed = discord.Embed(
      title=f"__*All Roles in this Guild {{{guild.name}}}*__", 
      description="\n• ".join(rolelist), 
      color=discord.Color.darker_grey())
      
    await ctx.send(embed=embed)
          
  @commands.command(name="roleperms", brief="{Get a List of Perms for a Role}")
  @commands.guild_only()
  @bot_perms()
  async def perms(self, ctx, *, role: discord.Role):
    """
    List of Perms for a Role
    """
    
    #perms = [perm.title().replace("_", " ") for perm, value in role.permissions '<:greenmark:738415677827973152>' if value else '<:redmark:738415723172462723>']
    perms = [f'{perm.title().replace("_", " ")} {("= <:greenmark:738415677827973152>" if value else "= <:redmark:738415723172462723>")}' for perm, value in role.permissions]
    
    embed = discord.Embed(
      color=discord.Color.darker_grey(), 
      title=f"Permissions for: `{role.name}`", 
      description="\n".join(perms))
          #title=f"Permissions for `{role.name}`", 
          #description=f"{list(role.permissions)}",)
          
    #embed.add_field(name="Permission for: {role.mention}", value="\n = ".join(perms))
    
    embed.timestamp = datetime.datetime.utcnow()
      
    await ctx.send(embed=embed)
      
  @perms.error
  async def perms_error(self, ctx, error):
      if isinstance(error, commands.BadArgument):
          await ctx.send("That isn't a valid role")
          
  #@commands.command()
  #@commands.guild_only()
  #@commands.has_permissions(manage_roles=True)
  #async def rolecolor(self, ctx, hex: discord.Color, *, role: discord.Role):
      
          
  @commands.command(name="createrole", brief="{Create a New Role}")
  @commands.guild_only()
  @bot_perms()
  @commands.has_permissions(manage_roles=True)
  async def create(self, ctx, *, role):
    """
    Creates a Role
    """
    guild = ctx.guild
    msg = await guild.create_role(name=None)
    await ctx.send(f"{msg.mention} was successfully created")
     
  @commands.command(name="deleterole", brief="{Delete a Role}")
  @commands.guild_only()
  @bot_perms()
  @commands.has_permissions(manage_roles=True)
  async def delete(self, ctx, *, role: discord.Role):
    """
    Deletes a Role
    """
    await role.delete()
    await ctx.send(f"{role} was successfully deleted")
          
def setup(bot):
    bot.add_cog(Role(bot))
