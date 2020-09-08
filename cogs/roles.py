#•----------Modules----------•#
import discord

from discord.ext.commands import command, Cog, guild_only, has_permissions, bot_has_permissions, BadArgument, Greedy, \
cooldown, BucketType

import asyncio

from datetime import datetime

import typing

from typing import Union, Optional

#•----------Commands----------•#

class Role(Cog, name="Role Category"):
  
    """`{Commands for Managing Roles}`"""
  
    def __init__(self, bot):
        self.bot = bot

    @command(
        name="createrole", 
        brief="{Create a New Role}", 
        usage="createrole <role_name> (color) (reason_for_creating)", 
        aliases=['rcreate', 'rolenew', 'newrole'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
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
    @cooldown(1, 1.5, BucketType.user)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def delete(self, ctx, *, role: discord.Role):
  
        await role.delete()
    
        await ctx.send(f"{role} was successfully deleted")

    @command(
        name="addrole", 
        brief="{Add a Role to a Member}", 
        usage="addrole <member> <role>", 
        aliases=['addr', 'radd'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
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
      
    @command(
        name="removerole", 
        brief="{Remove a Role from a Member}", 
        usage="removerole <member(s)> <role_name>", 
        aliases=['roleremove', 'rremove'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
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

    @command(
        brief="{Assign a Role to a Specified role}", 
        usage="raall <giving_role> <existing_role>", 
        aliases=['roleassign', 'rassign'])
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True, use_external_emojis=True)
    @cooldown(1, 1.5, BucketType.user)
    async def raall(self, ctx, giving: discord.Role, *, exist: discord.Role):
        
        greenmark = "<:greenmark:738415677827973152>" 
        
        redmark = "<:redmark:738415723172462723>"
        
        #Iterate through the members
        #Inside of the existing role
        for member in exist.members:
            #Add the role we're giving to 
            #Everyone with exist role
            await member.add_roles(giving)
        
        #Make embed
        e = discord.Embed(
            description=f"{greenmark} __*Successfully gave the **{giving.mention}** Role to everyone with the **{exist.mention}** Role*__")
        await ctx.send(embed=e)
        
    @command(
        brief="{Remove a Role from Everyone with the Specified Role}", 
        usage="rrall <role_to_remove> <role_to_remove_from>",
        aliases=['rremoveall'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    @bot_has_permissions(manage_roles=True, use_external_emojis=True)
    @has_permissions(manage_roles=True)
    async def rrall(self, ctx, removing: discord.Role, *, _from: discord.Role):
        
        greenmark = "<:greenmark:738415677827973152>"
        
        #Iterate through the members
        #Inside of removing role
        for member in _from.members:
            #Remove the role from every member
            await member.remove_roles(removing)
        
        #Make embed
        e = discord.Embed(
            description=f"{greenmark} __*Successfully Removed **{removing.mention}** from everyone with the **{_from.mention}** Role*__")
        await ctx.send(embed=e)
    
    @command(
        name="roleposition", 
        brief="{Change the Position of a Role}", 
        usage="roleposition <role> <#position>", 
        aliases=['rposition', 'rpos', 'rolepos']) 
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def position(self, ctx, role: discord.Role, *, position: int):
      
        redmark = "<:redmark:738415723172462723>" 
        
        greenmark = "<:greenmark:738415677827973152>"
        
        mem = ctx.author
        
        if not position:
            e = discord.Embed(
                description=f"{redmark} __*{mem.mention}, you need to give a valid number*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
          
        rolepos = role.position
        
        await role.edit(position=position, reason="Changing position of a role")
        
        e = discord.Embed(
            description=f"{greenmark} __*Successfully changed position for **{role.mention}** from **{rolepos}** to **{role.position}** *__")
        await ctx.send(embed=e)
    
    @command(
        name="rolename", 
        brief="{Change the Name of a Role}", 
        usage="rolename <role> <new_name>", 
        aliases=['rname'])
    @guild_only()
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    @cooldown(1, 1.5, BucketType.user)
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
    
    @command(
        name="rolecolor", 
        brief="{Change the color of a Role}", 
        usage="rolecolor <color> <role_name>", 
        aliases=['rcolor'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
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
            
#•---------Custom Error Handling----------•#

    @add.error
    async def add_error(self, ctx, error):
      if isinstance(error, BadArgument):
          e = discord.Embed(
              color=0x420000, 
              description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"role_name"`\n• Valid Syntax: `{ctx.prefix}addrole <member> <role_name>`')
          
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

    @name.error
    async def name_error(self, ctx, error):
      if isinstance(error, BadArgument):
      
          e = discord.Embed(
              color=0x420000, 
              description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role name"``\n• Valid Syntax: `{ctx.prefix}rolename <new_name> <role_name>`')
        
          e.timestamp = datetime.utcnow()
      
          await ctx.send(embed=e)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, BadArgument):

            e = discord.Embed(
                color=0x420000, 
                description=f'Either:\n• Role wasn\'t found\n• Roles including spaces must be surrounded with `"<role_name>"`\n• Valid Syntax: `{ctx.prefix}role remove <member> <role_name>`')
            
            e.timestamp = datetime.utcnow()
        
            await ctx.send(embed=e)

#•-----------Setup/Add this Cog-----------•#
          
def setup(bot):
    bot.add_cog(Role(bot))
