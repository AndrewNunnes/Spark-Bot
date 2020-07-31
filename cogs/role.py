import discord
from discord.ext import commands
import asyncio
import datetime

class Role(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_roles=True)
  async def addrole(self, ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"Successfully gave {role.mention} to: `{member.display_name}`")
    
  @addrole.error
  async def addrole_error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send("Looks like that role doesn't exist or that member isn't in this server")
      
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_roles=True)
  async def removerole(self, ctx, member: discord.Member, *, role: discord.Role):
      """
      Removes a role from a user
      """
      await member.remove_roles(role)
      await ctx.send(f"Successfully removed {role.mention} from: `{member.display_name}`")
      
  @removerole.error
  async def removerole_error(self, ctx, error):
      if isinstance(error, commands.BadArgument):
          await ctx.send("Looks like that role doesn't exist, or that's the wrong member")
          
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
          
  @commands.command()
  @commands.guild_only()
  async def roleinfo(self, ctx, *, role: discord.Role):
      """
      Pulls info about a role
      """
      embed = discord.Embed(
          title=f"Info on {role.mention}", 
          description=f"**>Role ID:** {role.id}\n**>Server it belongs to:** {ctx.guild}\n**>Does it Display from others?:** {role.hoist}\n**>Position:** {role.position}\n**>Created at:** {role.created_at.strftime('%d/%m/%Y')}", 
          color=discord.Color.darker_grey())
      embed.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=embed)
      
  @roleinfo.error
  async def roleinfo_error(self, ctx, error):
      if isinstance(error, commands.BadArgument):
          await ctx.send("That isn't a valid role")
          
  @commands.command()
  @commands.guild_only()
  async def rolelist(self, ctx):
    guild = ctx.guild
    
    rolelist = [role.mention for role in guild.roles] # List of the names for the roles in the guild
    
    embed = discord.Embed(
      title=f"__*All Roles in this Guild {{{guild.name}}}*__", 
      description="\n• ".join(rolelist), 
      color=discord.Color.darker_grey())
      
    await ctx.send(embed=embed)
          
  @commands.command()
  @commands.guild_only()
  async def roleperms(self, ctx, *, role: discord.Role):
    
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
      
  @roleperms.error
  async def roleperms_error(self, ctx, error):
      if isinstance(error, commands.BadArgument):
          await ctx.send("That isn't a valid role")
          
  #@commands.command()
  #@commands.guild_only()
  #@commands.has_permissions(manage_roles=True)
  #async def rolecolor(self, ctx, hex: discord.Color, *, role: discord.Role):
      
          
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_roles=True)
  async def createrole(self, ctx, *, role):
      guild = ctx.guild
      msg = await guild.create_role(name=None)
      await ctx.send(f"{msg.mention} was successfully created")
     
  @commands.command()
  @commands.guild_only()
  @commands.has_permissions(manage_roles=True)
  async def deleterole(self, ctx, *, role: discord.Role):
      await role.delete()
      await ctx.send(f"{role} was successfully deleted")
          
def setup(bot):
    bot.add_cog(Role(bot))
