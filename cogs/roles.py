#•----------Modules----------•#
import discord

from discord.ext.commands import command, Cog, guild_only, has_permissions, bot_has_permissions, BadArgument, Greedy, \
cooldown, BucketType

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
      usage="roleposition <role> <#position>", 
      aliases=['rposition', 'rpos', 'rolepos']) 
    @guild_only()
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
        brief="{Assign a Role to a Specified role}", 
        usage="raall <giving_role> <existing_role>", 
        aliases=['roleassign', 'rassign'])
    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True, use_external_emojis=True)
    @cooldown(1, 2.5, BucketType.user)
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
    @cooldown(1, 2.5, BucketType.user)
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
      name="rolename", 
      brief="{Change the Name of a Role}", 
      usage="rolename <role> <new_name>")#description="{Change the name of a Role}")
    @guild_only()
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    @cooldown(1, 2.5, BucketType.user)
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
        brief="{Get a List of Perms for a Role/Member}", 
        usage="perms <role>/(member)", 
        aliases=['permission', 'permissions'])
    @guild_only()
    @bot_has_permissions(use_external_emojis=True)
    async def perms(self, ctx, *, item: Optional[Union[discord.Role, discord.Member]]):
        
        greenmark = "<:greenmark:738415677827973152>" 
        redmark = "<:redmark:738415723172462723>"
        garbage = "<:trash:734043301187158082>"
        
        #Make optional to mention a member
        item = item if item else ctx.author
        
        if isinstance(item, discord.Member):
            #Iterating through list of guild perms
            perms = [f"{perm.title().replace('_', ' ')} = {greenmark if value else redmark}" for perm, value in item.guild_permissions]
        
        else:
            #Iterating through list of general perms
            perms = [f"{perm.title().replace('_', ' ')} = {greenmark if value else redmark}" for perm, value, in item.permissions]
        
        #Split the list of perms into 2
        middle = len(perms) // 2
        f_half = perms[:middle]
        s_half = perms[middle:]
        
        #List of contents go through
        #Inside of our embeds
        contents = [f_half, s_half]
        
        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            description=f"{contents[cur_page-1]}")
            
        e.set_author(
            name=f"Page {cur_page}/{pages}")
        
        #Store the first embed we're sending
        msg = await ctx.send(embed=e)
        
        #Reactions to add
        emotes = ['⬅️', '➡️', '⏹']
        for react in emotes:
            #Add the reactions
            await msg.add_reaction(react)
        
        #Custom check to check for the author of the command
        #And check for the right emojis
        def checkauth(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await msg.edit(embed=err)
                await msg.clear_reactions()
                break
              
            else:
                #Check for the specific emoji
                #And if the user isn't trying to go to the negative side 
                #Of pages
                if str(reaction.emoji) == '⬅️' and cur_page > 1:
                    await msg.remove_reaction(reaction, user)
                    cur_page -= 1
                    
                    e = discord.Embed(
                        description=f"{contents[cur_page-1]}")
                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    
                    await msg.edit(embed=e)
                #Check for the specific emoji
                #And if the user tries to go forward too much
                elif str(reaction.emoji) == '➡️' and cur_page != pages:
                    await msg.remove_reaction(reaction, user)
                    cur_page += 1
                    
                    e = discord.Embed(
                        description=f"{contents[cur_page-1]}")
                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                        
                    await msg.edit(embed=e)
                
                #Used to delete the embed
                elif str(reaction.emoji) == '⏹':
                    await msg.clear_reactions()
                    e = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    await msg.edit(embed=e, delete_after=5)
                
                else:
                    await msg.remove_reaction(reaction, user)
    
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
