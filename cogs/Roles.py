#•----------Modules----------•#
import discord

from discord.ext.commands import command, Cog, guild_only, has_permissions, bot_has_permissions, BadArgument

import asyncio

from datetime import datetime

import typing

from typing import Union

#•----------Commands----------•#

class Role(Cog, name="Role Management"):
  
    """😱 `{Commands for Managing Roles}`"""
  
    def __init__(self, bot):
        self.bot = bot
    
    @command(
      name="roleposition", 
      brief="{Change the Position of a Role}", 
      usage="roleposition <#position>") #usage="{Change the position of a Role}")
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def position(self, ctx, role: discord.Role, *, position: int):
      pass
    
    @command(
      name="rolename", 
      brief="{Change the Name of a Role}", 
      usage="rolename <role> <new_name>")#description="{Change the name of a Role}")
    @guild_only()
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def name(self, ctx, role: discord.Role, *, name=None):
    
      #If user doesn't give a new name
      if name is None:
          await ctx.send("You have to give this role a name")
          return
    
      #If they give a name
      elif name is not None:
          rolename = role.name
    
          #Edit the role
          await role.edit(name=name)
    
          e = discord.Embed(
              description=f"**Successfully changed {rolename} to {name}**")
      
          e.timestamp = datetime.utcnow()
    
          await ctx.send(embed=e)
    
    @name.error
    async def name_error(self, ctx, error):
      if isinstance(error, BadArgument):
      
        e = discord.Embed(
          color=discord.Color.dark_red(), 
          description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role name"``\n• Valid Syntax: `{ctx.prefix}rolename <new_name> <role_name>`')
        
        e.timestamp = datetime.utcnow()
      
        await ctx.send(embed=e)
      
    @command(
      name="rolecolor", 
      brief="{Change the color of a Role}", 
      usage="rolecolor <color> <role_name>")
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def color(self, ctx, color: discord.Color, *, role: discord.Role):
    
        if not color:
            await ctx.send("You gotta give a new color for the role")
            return
       
        #If they do give a color 
        if color:
        
            #Make a few helpful variables
            rolecolor = role.color
    
            rolemention = role.mention
    
            #Edit the role
            await role.edit(color=color)
    
            #Make and send embed
            e = discord.Embed(
                description=f"Successfully changed colors for {rolemention}{{`{rolecolor}`}} to {{`{color}`}}")
      
            e.timestamp = datetime.utcnow()
      
            await ctx.send(embed=e)
      
    @color.error
    async def color_error(self, ctx, error):
      if isinstance(error, BadArgument):
      
        e = discord.Embed(
          color=discord.Color.dark_red(), 
          description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role_name>"`\n• Valid Syntax: `{ctx.prefix}role color <color> <role_name>`')
          
        e.timestamp = datetime.utcnow()
        
        await ctx.send(embed=e)
    
    @command(
      name="addrole", 
      brief="{Add a Role to a Member}", 
      usage="addrole <member> <role>")
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def add(self, ctx, member: discord.Member, *, role: discord.Role):
    
        await member.add_roles(role)
    
        await ctx.send(f"Successfully gave {role.mention} to: `{member}`")
    
    @add.error
    async def add_error(self, ctx, error):
      if isinstance(error, BadArgument):
        e = discord.Embed(
          color=discord.Color.dark_red(), 
          description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"role_name"`\n• Valid Syntax: `{ctx.prefix}addrole <member> <role_name>`')
          
        e.timestamp = datetime.utcnow()
        
        await ctx.send(embed=e)
      
    @command(
      name="removerole", 
      brief="{Remove a Role from a Member}", 
      usage="removerole <member> <role_name>", 
      aliases=['roleremove', 'rremove'])
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def remove(self, ctx, member: discord.Member, *, role: discord.Role):
      
        #Remove role from member
        await member.remove_roles(role)
      
        await ctx.send(f"Successfully removed {role.mention} from: `{member}`")
      
    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, BadArgument):
        
          e = discord.Embed(
            color=discord.Color.dark_red(), 
            description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role_name>"`\n• Valid Syntax: `{ctx.prefix}role remove <member> <role_name>`')
            
          e.timestamp = datetime.utcnow()
        
          await ctx.send(embed=e)
          
    @command(
      name="roleinfo", 
      brief="{Get Info on a Role}", 
      usage="roleinfo <role>", 
      aliases=['ri', 'rinfo'])
    @guild_only()
    async def info(self, ctx, *, role: discord.Role):
          
        #See when the role was created
        role_created = f"{role.created_at.strftime('%a/%b %d/%Y • %I:%M %p')}"
        
        #List number of non-bots
        humans = len(list(filter(lambda h: not h.bot, role.members)))
        
        #List number of bots
        bots = len(list(filter(lambda b: b.bot, role.members)))
        
        #If there is more than 15 members
        if len(role.members) > 25:
            length = len(role.members) - 25
        
            human_list = f"{' , '.join(map(str, (member.mention for member in list(reversed(role.members))[:25])))} and **{length}** more"
        #If there is less than 25 members
        else:
            human_list = f"{' , '.join(map(str, (member.mention for member in (list(reversed(role.members[1:]))))))}"
        
        #If there is no members 
        human_lt = "No Members" if human_list == "" else human_list
        
        #Custom emojis
        check = "<:greenmark:738415677827973152>"
        x = "<:redmark:738415723172462723>"
        
        #Using emojis from above
        #To show any bools
        mentionable = check if role.mention else x
        hoisted = check if role.hoist else x
        
        e = discord.Embed(
            description=f"**General Info for {role.mention} {{Color In Hex > {role.color}}}**")
      
        #Make fields
        fields = [("ID", role.id, True),
        
                  ("Misc", 
                  f"\nMentionable? {mentionable}" +
                  f"\nDisplays from Others? {hoisted}", True), 
      
                  ("Position", role.position, True), 
                
                  (f"Members w/{role.name} {{{len(role.members)}}}", 
                  f"\nHumans: {humans}" +
                  f"\nBots: {bots}", False), 
                  
                  (f"List of Members with this Role", human_lt, False)]
                  
        #Show when role was created
        e.set_footer(
            text=f"Role Created At | {role_created}")
            
        e.set_author(
            name=f"Requested by {ctx.author}", 
            icon_url=ctx.author.avatar_url)
        
        #Add fields     
        for name, val, inl in fields:
            e.add_field(
                name=name, 
                value=val, 
                inline=inl)
      
        await ctx.send(embed=e)
      
    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("That isn't a valid role")
          
    @command(
      name="rolelist", 
      brief="{Get a List of All the Roles in the Server}", 
      usage="rolelist")
    @guild_only()
    async def _list(self, ctx):
    
      guild = ctx.guild
    
      #Variable for getting roles in guild
      rolelist = guild.roles
    
      #Check if there is 
      #Over 25 roles in the guild
      if len(rolelist) > 25:
          #Get the length of remaining roles
          length = len(rolelist) - 25
        
          role = f"{' • '.join(map(str, (role.mention for role in list(reversed(rolelist))[:20])))} and **{length}** more"
        
      #If there is less than 25 roles
      #In the guild
      else:
          role = f"{' • '.join(map(str, (role.mention for role in list(reversed(rolelist[1:])))))}"
        
      #Check if there is no roles to display
      roles = "No Roles" if role == "" else role
    
      #Make and send embed
      e = discord.Embed(
          title=f"__*Roles in {{{guild.name}}}*__\n**Total {{{len(rolelist)}}}", 
          description=roles)
          
      e.timestamp = datetime.utcnow()
      
      await ctx.send(embed=e)
          
    @command(
        name="roleperms", 
        brief="{Get a List of Perms for a Role}", 
        usage="roleperms <role>", 
        aliases=['rolepermission', 'rperms', 'rolepermissions'])
    @guild_only()
    @bot_has_permissions(use_external_emojis=True)
    async def perms(self, ctx, *, role: discord.Role):
    
        #Iterating through list of perms
        perms = [f'{perm.title().replace("_", " ")} {("= <:greenmark:738415677827973152>" if value else "= <:redmark:738415723172462723>")}' for perm, value in role.permissions]
    
        #Make and send embed
        e = discord.Embed(
            color=discord.Color.darker_grey(), 
            title=f"Permissions for: `{role.name}`", 
            description="\n\n".join(perms))
    
        e.timestamp = datetime.datetime.utcnow()
      
        await ctx.send(embed=e)
      
    @perms.error
    async def perms_error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("That isn't a valid role")
          
    @command(
        name="createrole", 
        brief="{Create a New Role}", 
        usage="createrole <role_name> (color) (reason_for_creating)")
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def create(self, ctx, name=None, color: discord.Color=None, *, reason):
    
        guild = ctx.guild
        
        if reason is None:
            await ctx.send("You need to give a reason for creating this role")
            return
    
        if name is None:
            await ctx.send("You have to give a name for the role")
            return
    
        if name is not None:
      
            #Create the new role
            msg = await guild.create_role(name=name, color=color, reason=reason)
    
            await ctx.send(f"{msg.mention} was successfully created")
     
    @command(
        name="deleterole", 
        brief="{Delete a Role}", 
        usage="deleterole <role>", 
        aliases=['roledelete', 'rdelete', 'roledel'])
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def delete(self, ctx, *, role: discord.Role):
  
        await role.delete()
    
        await ctx.send(f"{role} was successfully deleted")
          
def setup(bot):
    bot.add_cog(Role(bot))
