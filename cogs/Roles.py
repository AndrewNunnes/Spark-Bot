----------Modules----------•#
import discord

from discord.ext.commands import command, Cog, guild_only, has_permissions, bot_has_permissions, BadArgument, Greedy

import asyncio

from datetime import datetime

import typing

from typing import Union, Optional

#•----------Functions----------•#

#•----------Commands----------•#

class Role(Cog, name="Role Category"):
  
    """`{Commands for Managing Roles}`"""
  
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
              color=0x420000, 
              description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role name"``\n• Valid Syntax: `{ctx.prefix}rolename <new_name> <role_name>`')
        
          e.timestamp = datetime.utcnow()
      
          await ctx.send(embed=e)
      else:
          raise(error)
      
    @command(
      name="rolecolor", 
      brief="{Change the color of a Role}", 
      usage="rolecolor <color> <role_name>")
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def color(self, ctx, color: discord.Color, *, role: discord.Role):
        
        #If they don't give a color
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
              color=0x420000, 
              description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role_name>"`\n• Valid Syntax: `{ctx.prefix}role color <color> <role_name>`')
          
          e.timestamp = datetime.utcnow()
        
          await ctx.send(embed=e)
      else:
          raise(error)
    
    @command(
      name="addrole", 
      brief="{Add a Role to a Member}", 
      usage="addrole <member> <role>", 
      aliases=['addr', 'radd'])
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def add(self, ctx, member: discord.Member, *, role: discord.Role):
      
        #If author doesn't give at least 1 member
        if not member:
            await ctx.send("You have to give a member to give a role to")
            return

        await member.add_roles(role)
        
        e = discord.Embed(
            color=0x420000, 
            description=f"<:greenmark:738415677827973152> __*Successfully gave {role.mention} to {member.mention}*__")
            
        e.timestamp = datetime.utcnow()
        
        await ctx.send(embed=e)

    @add.error
    async def add_error(self, ctx, error):
      if isinstance(error, BadArgument):
          e = discord.Embed(
              color=0x420000, 
              description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"role_name"`\n• Valid Syntax: `{ctx.prefix}addrole <member> <role_name>`')
          
          e.timestamp = datetime.utcnow()
        
          await ctx.send(embed=e)
      else:
          raise(error)
      
    @command(
      name="removerole", 
      brief="{Remove a Role from a Member}", 
      usage="removerole <member(s)> <role_name>", 
      aliases=['roleremove', 'rremove'])
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def remove(self, ctx, member: discord.Member, *, role: discord.Role):
        
        #If a member isn't given
        if not member:
            await ctx.send("You have to give at least 1 member to remove this role from")
            return
        
        else:
            #Remove role from member
            await member.remove_roles(role)
        
            e = discord.Embed(
                color=0x420000, 
                description=f"<:greenmark:738415677827973152> __*Successfully removed {role.mention} from {member.mention}*__")
                
            e.set_thumbnail(
                url=member.avatar_url)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, BadArgument):

            e = discord.Embed(
                color=0x420000, 
                description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role_name>"`\n• Valid Syntax: `{ctx.prefix}role remove <member> <role_name>`')
            
            e.timestamp = datetime.utcnow()
        
            await ctx.send(embed=e)
        else:
            raise(error)
          
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
    
        #perms = [f'{perm.title().replace("_", " ")} {("= <:greenmark:738415677827973152>" if value else "= <:redmark:738415723172462723>")}' for perm, value in role.permissions]
        
        #Make embed
        e = discord.Embed(
            description=f"__*Permissions for {role.mention} {{*Color in Hex: {role.color}*}}*__")
        
        #Iterate through list of perms
        for perm, value in role.permissions:
            
            #Use our custom emojis
            #To show if perms are true or not
            green_red = f'{("True <:greenmark:738415677827973152>" if value else "False <:redmark:738415723172462723>")}'
            
            #Make fields
            fields = [(f'{perm.title().replace("_", " ")}', green_red, True)]
            
            #Add fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
        e.set_thumbnail(
            url=ctx.author.avatar_url)
            
        e.set_footer(
            text=f"Requested by {ctx.author}")
  
        e.timestamp = datetime.utcnow()
      
        await ctx.send(embed=e)
      
    @perms.error
    async def perms_error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("That isn't a valid role")
        else:
            raise(error)
          
    @command(
        name="createrole", 
        brief="{Create a New Role}", 
        usage="createrole <role_name> (color) (reason_for_creating)")
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def create(self, ctx, name=None, color: discord.Color=None, *, reason: Optional[str]="No Reason Provided"):
    
        guild = ctx.guild

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
