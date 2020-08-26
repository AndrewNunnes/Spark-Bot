
#•----------Modules-----------•#

import discord

from discord.ext import commands

from discord.ext.commands import Greedy 

import asyncio

from asyncio import sleep

import datetime

from datetime import timedelta

from typing import Optional

import cogs._json

#•----------Class----------•#

class Management(commands.Cog):
  
    """⚠️ `{Commands for Moderating the Server}`"""
    def __init__(self, bot):
        self.bot = bot
        
        #Make a variable to get functions from database
        #Makes stuff a lot easier
        self.db = self.bot.get_cog('Database')
        
#•----------Command Menus----------•#
#•--{Gets the cogs and Show their Commands--•#

    @commands.command(
        brief="{Menu for Welcome Messages}", 
        usage="welcomemenu", 
        aliases=['wlcmemu', 'wcmenu']
    )
    @commands.guild_only()
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def welcomemenu(self, ctx):
        
        #Get the Welcome Cog
        cog = self.bot.get_cog('Welcome')
        
        #Make the embed
        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            color=0x420000)
        
        #Iterate through all (sub)commands 
        #For the cog we get
        for c in cog.walk_commands():
            
            #Make our fields
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.brief}`", f"{c.usage}", True)]
            
            #Iterate through our fields list
            for n, v, i in fields:
                #Add the fields
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
                    
        e.timestamp = datetime.datetime.utcnow()
        
        await ctx.send(embed=e)

    @commands.command(
        brief="{Menu for Goodbye Messages}", 
        usage="goodbyemenu", 
        aliases=['byemenu', 'gbmenu']
    )
    @commands.guild_only()
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def goodbyemenu(self, ctx):

        cog = self.bot.get_cog('Goodbye')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            color=0x420000)
        
        for c in cog.walk_commands():
            
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.brief}`", f"{c.usage}", True)]
            
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
        e.timestamp = datetime.datetime.utcnow()
        
        await ctx.send(embed=e)

    @commands.guild_only()
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def logsmenu(self, ctx):

        cog = self.bot.get_cog('Logging')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__",
            color=0x420000)
        
        #Iterate through all commands including subcommands 
        #Inside of that cog
        for c in cog.walk_commands():
            
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
        e.timestamp = datetime.datetime.utcnow()
        
        await ctx.send(embed=e)

    @commands.command(
      brief="{Menu for Role Management}", 
      usage="role")
    @commands.guild_only()
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def role(self, ctx):
      
        cog = self.bot.get_cog('Role Management')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__",
            color=0x420000)
      
        for c in cog.walk_commands():
          
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            for name, val, i in fields:
                e.add_field(
                    name=name, 
                    value=val, 
                    inline=i)
        
        e.timestamp = datetime.datetime.utcnow()
      
        await ctx.send(embed=e)
      
    @commands.command(
      brief="{Menu for Managing Categories}", 
      usage="categorymenu", 
      aliases=['categmenu'])
    @commands.guild_only()
    async def categorymenu(self, ctx):
      
        cog = self.bot.get_cog('Category')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            color=0x420000)
            
        for c in cog.walk_commands():
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.timestamp = datetime.datetime.utcnow()
      
        await ctx.send(embed=e)
      
    @commands.command(
      brief="{Menu for Managing Channels}", 
      usage="channelmenu", 
      aliases=['chmenu'])
    @commands.guild_only()
    async def channelmenu(self, ctx):
      
        cog = self.bot.get_cog('Channels')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            color=0x420000)
        
        for c in cog.walk_commands():
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.timestamp = datetime.datetime.utcnow()
      
        await ctx.send(embed=e)
      
#•----------Management Commands----------•#
      
    @commands.command(
      brief="{Change the Bot's Prefix}", 
      usage="prefix <new_prefix>")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    #@bot_perms()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, *, pre):
        data = cogs._json.read_json('prefixes')
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, 'prefixes')

        if pre is None:
            await ctx.send(f"The server prefix is set to {ctx.prefix}. Use {ctx.prefix}prefix to change it")
            
        elif pre is not None:
        
            await ctx.send(f"The server prefix has been set to `{pre}`. Use `{pre}prefix <newprefix>` to change it again")
            
#•----------Warn System----------•#
            
    @commands.command(
      brief="{Warn a User}", 
      usage="warn <user> (reason)", 
      aliases=['addwarn', 'warnuser'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: Optional[str]="No Reason Provided"):
        
        #If a member isn't provided
        if not member:
            await ctx.send("You have to give a reason to warn this member")
            return
        
        #If the reason is too long
        if len(reason) > 350:
            await ctx.send("Reason has to be less than 350 Characters")
            return
        
        #If the author's top role
        #Is under the member's top role
        if ctx.author.top_role.position < member.top_role.position:
            await ctx.send("You don't have permissions to warn this member")
            return
        
        #If the author tries to warn the owner
        #Of the server
        if ctx.author.id != ctx.guild.owner.id:
            await ctx.send("You can't warn the Owner of the Server")
            return
        
        #If the author tries to warn
        #Themselves
        if ctx.author == member:
            await ctx.send("You can't warn yourself")
            return

        #Add to member's total warns
        await self.db.add_warns(member.id, ctx.author.id, reason, ctx.guild.id)
        
        #Embed to try and send to member
        #Wrapped in try/except in case
        #It tries to send to a bot
        try:
            
            #Get member's total warns
            total_warns = len(await self.db.get_warns(member.id, ctx.guild.id))
        
            e = discord.Embed(
              color=0x420000, 
              title=f"⚠️ **You've been Warned in {ctx.guild}!**")
            #Make fields
            fields = [("__*Warned By*__", ctx.author, True), 
            
                    ("__*Reason*__", reason, True), 
                    
                    ("__*Total Warns*__", total_warns, True)]
            
            #Add fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
          
            e.timestamp = datetime.datetime.utcnow()
        
            await member.send(embed=e)
            
        except Exception as e:
            print(e)
        
        #Get member's total warns
        total_warns = len(await self.db.get_warns(member.id, ctx.guild.id))

        #Make embed
        e = discord.Embed(
            color=0x420000, 
            description=f"⚠️ **{member}** has been warned. They now have **{total_warns} warn(s)**")
        
        #Make embed fields
        fields = [("__*Warned by*__", ctx.author, True), 
        
                ("__*Reason*__", reason, True)]
                  
        for name, value, inline in fields:
          
            e.add_field(
                name=name, 
                value=value, 
                inline=inline)
            
        e.timestamp = datetime.datetime.utcnow()
        
        e.set_footer(
          text=member, 
          icon_url=member.avatar_url)
        
        await ctx.send(embed=e)
        
    @commands.command(
      brief="{List of Warns a User has", 
      usage="warns <member>", 
      aliases=['warnlist', 'listwarns'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True, use_external_emojis=True)
    async def warns(self, ctx, member: Optional[discord.Member]):
        
        #Makes it optional to mention a member
        member = ctx.author if not member else member
        
        #Get the list of warns from database
        warn_list = await self.db.get_warns(member.id, ctx.guild.id)

        #Make embed
        e = discord.Embed(
            description=f"**{member.mention}'s List of Warns : {{{len(warn_list)}}} Total**")
            
        e.set_thumbnail(
            url=member.avatar_url)

        #Check if there is any warns
        #In database
        if len(warn_list) == 0:
        
            e = discord.Embed(
                color=0x420000, 
                description=f"<:redmark:738415723172462723> __*{member.mention} doesn't have any warns to display*__")
          
            e.set_thumbnail(
                url=ctx.author.avatar_url)
          
            await ctx.send(embed=e)
            return
          
        #Iterate through our warn_list variable
        for warning in warn_list:
          
            #Define the moderator
            #Who warned
            mod = self.bot.get_user(id=warning[1])

            #If there isn't a reason
            if warning[2] is None:
                reason = "No Reason"
            #If there is a warning
            else:
                reason = warning[2]
                
            fields = [(f"**Warn Case {{{warning[3]}}}**", 
                    f"*Warned By: {mod}*" +
                    f"\n*Reason: {reason}*",
                    True)]
            #Add fields
            for n, v, i in fields:
                
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
            e.set_footer(
                text=f"ID: {member.id}")

        await ctx.send(embed=e)
    
    @commands.command(
        brief="{Delete a Specific Warn}", 
        usage="delwarn <number_of_warn_case>", 
        aliases=['deletewarn', 'dwarn'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True, use_external_emojis=True)
    async def delwarn(self, ctx, member: discord.Member, *, number: int):
        
        #Get warns from database
        get_warns = await self.db.get_warns(member.id, ctx.guild.id)
        
        #If a member isn't given
        if not member:
            await ctx.send("You must give a member to delete a warn for")
            return
        
        if not number:
            await ctx.send("You must give the number of the **Warn Case** to delete\nExample: `!delwarn <@user <2>`")
            return

        #If the member has no warns
        if len(get_warns) == 0:
          
            e = discord.Embed(
                description=f"<:redmark:738415723172462723> __*{member.mention} doesn't have any warns to delete*__")
                
            await ctx.send(embed=e)
            
            return
          
        else:
            
            #Delete the specific warn
            await self.db.delete_warn(number)
            
            e = discord.Embed(
                description=f"__*Deleting Warn Case **{number}** for {member.mention}...*__")
            
            m = await ctx.send(embed=e)
            
            await asyncio.sleep(1.5)
            
            ed = discord.Embed(
                description=f"<:greenmark:738415677827973152> __*Successfully Deleted Warn Case **{number}** from {member.mention}*__")
                
            e.set_footer(
                text=f"Warn Case {number} Deleted From {member.mention}")
            e.timestamp = datetime.datetime.utcnow()
            
            await m.edit(embed=ed)
        
    @commands.command(
        brief="{Clear all Warns for a User}", 
        usage="clearwarns <user>", 
        aliases=['clearwrn', 'clearwrns'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True, use_external_emojis=True)
    async def clearwarns(self, ctx, member: discord.Member):
        
        #If a member isn't given
        if not member:
            await ctx.send("You must give a member to clear warns for")
            return
          
        #Function used to check
        #If user has any warns
        #To clear
        get_warns = await self.db.get_warns(member.id, ctx.guild.id)
        
        #If the user has no warns at all
        if len(get_warns) == 0:
            e = discord.Embed(
                description=f"<:redmark:738415723172462723> __*{member.mention} doesn't have any warns to delete*__")
                
            await ctx.send(embed=e)
            return
        
        #If they do have any warns
        else:
          
            #Clear all the member's warns
            await self.db.clear_warns(member.id, ctx.guild.id)
            
            e = discord.Embed(
                description=f"**Deleting All Warns for {member.mention}...**")
            
            m = await ctx.send(embed=e)
            
            await asyncio.sleep(1)
            
            e = discord.Embed(
                description=f"<:greenmark:738415677827973152> __*Successfully Deleted **{len(get_warns)}** Warn(s) from {member.mention}*__")
                
            await m.edit(embed=e)
        
#•----------User Management----------•#
  
    @commands.command(
      brief="{Kicks a User from the Guild}", 
      usage="kick <user> (reason_message)")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason):
      
        #Checking if the user tries to 
        #Kick themselves
        if ctx.author == member:
            await ctx.send("You cannot kick yourself.")
            return
          
        #Making sure user gives a reason
        #To kick the user first
        if reason is None:
            await ctx.send("You gotta give a reason to kick this member")
            return
        #await can_execute_action(user, target):
            #await ctx.send("You can't kick this user due to role hierarchy")
            #return
          
        try:
            #Sending the member this message
            await member.send(f'You\'ve been kicked from `{ctx.guild.name}` for `{reason}`')
        except Exception:
            pass

        #Kicking the member
        await member.kick()
        
        #Send embed
        e = discord.Embed(
              description=f'{member.name} has been kicked!', 
              color=0x420000)

        e.set_footer(text=f'Member: {member.name}\nID: {member.id}')

        e.timestamp = datetime.datetime.now()

        e.set_thumbnail(url=member.avatar_url)

        #Setting up the field
        fields = [("Member Kicked", member.name, True), 
                    ("Reason", reason, True), 
                    ("Kicked by", ctx.author, True)]

        #Adding the field
        for name, value, inline in fields:
              e.add_field(
                  name=name, 
                  value=value, 
                  inline=inline)
            
        await ctx.send(embed=e)

    @commands.command(
      brief="{Bans a User from the Guild}", 
      usage="ban <user> (reason_message)")
   # @bot_perms()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, user : discord.Member, *, reason=None):
        """`Bans a user from the server`"""

        if ctx.author == user:
            await ctx.send("You cannot ban yourself.")
            return

        if reason is None:
            await ctx.send("You gotta give a reason for banning this member")
            return

        #Try to send a message to the user
        try:
            e = discord.Embed(
              title="Banned ðŸ”¨", 
              description=f"__*You've been banned from `{ctx.guild.name}`\n\nReason: {reason}", 
              color=0x420000)
              
            e.timestamp = datetime.datetime.utcnow()
              
            await user.send(embed=e)
        except Exception as e:
            pass

        #Banning the user
        await user.ban()
            
        embed = discord.Embed(
              title=f'Banned {user.name}', 
              description=f'{user.mention} has been banned', 
              color=0x420000)
            
        embed.set_thumbnail(url=user.avatar_url)
            
        embed.timestamp = datetime.datetime.utcnow()
            
        await ctx.send(embed=embed)

    @commands.command(
      brief="{Unbans a User}", 
      usage="unban <user#1234>")
  #  @bot_perms()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """`Unbans a member from the server (!unban Example name#1234)`"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
     
                #Try to send a message to the user
                try:
                    await user.send(f"You've been unbanned from `{ctx.guild}`")
                
                except Exception:
                    pass

                await ctx.guild.unban(user)
                
                embed = discord.Embed(
                  title=f'Unbanned {user.name}', 
                  description=f'{user.mention} has been unbanned', 
                  color=discord.Color.dark_green())
                  
                embed.set_thumbnail(url=user.avatar_url)
                
                await ctx.send(embed=embed)

    @commands.command(
      brief="{Mute One or More User} [NOT DONE]", 
      usage="mute <user(s)> (time)", 
      aliases=['mutemember'])
    @commands.guild_only()
   # @bot_perms()
    @commands.has_permissions(mute_members=True)
    @commands.bot_has_permissions(mute_members=True)
    async def mute(self, ctx, targets: commands.Greedy[discord.Member], minutes: Optional[int], *, reason: Optional[str] = "No Reason Provided"):
      
        #If invoker doesn't give any members
        #To mute
        if not len(targets):
            await ctx.send("You have to give a member to mute")
            return
          
        #If invoker tries to mute themselves
        if ctx.author == targets:
            await ctx.send("You cannot mute yourself.")
            
        else:
          
            #Empty list to store
            #The members to unmute later on
            unmutes = []
            
            mute_role = discord.utils.get(ctx.message.guild.roles, name="Muted")
            
            #Iterate through the members
            #Mentioned
            for targ in targets:
                #If members don't have the mute role
                if not mute_role in targ.roles:
                    #Check the author has a higher role
                    #Then the members they're muting
                    if ctx.author.top_role.position > targ.top_role.position:
                      
                        #Get the roles
                        #The user has
                        roleids = ",".join([str(r.id) for r in targ.roles])
                        
                        #Amount of time
                        #To mute them for
                        endtime = datetime.datetime.utcnow() + timedelta(seconds=minutes * 60) if minutes else None
                        
                        #Execute the function
                        #From database
                        await self.db.mute_members(targ.id, roleids, getattr(end_time, "isoformat", lambda: None)())
                        
                        #Edit the member's roles
                        await targ.edit(roles=[mute_role])
                        
                        #Make the embed
                        e = discord.Embed(
                            title="**Member Muted**", 
                            color=0x420000)
                            
                        e.set_thumbnail(
                            url=targ.avatar_url)
                        
                        #Make the fields
                        fields = [("**Member Muted", targ.mention, False), 
                                  ("**Muted By**", ctx.author.mention, False), 
                                  ("**Duration**", f"{minutes:,} Minute(s)" if minutes else "Indefinite", False), 
                                  ("**Reason**", reason, False)]
                                  
                        #Add the fields
                        for name, val, inl in fields:
                            e.add_field(
                                name=name, 
                                value=val, 
                                inline=inl)
                        
                        #Send the embed
                        await ctx.send(embed=e)
                        
                        #Add the members
                        #To the empty list
                        #Of members to unmute
                        if minutes:
                            unmutes.append(targ)
            
    @commands.command(
      brief="{Manually unmute a User}", 
      usage="unmute <user>")
    @commands.guild_only()
    #@bot_perms()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member):
        """`Unmutes a user`"""
        rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
        dick = discord.utils.get(ctx.message.guild.roles, name = 'Verified Member')
        if rolem in user.roles:
            embed = discord.Embed(title=f'User {user.name} has been manually unmuted.', color=discord.Color.dark_green())
            embed.add_field(name="Welcome back!", value=":open_mouth:")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
            await user.remove_roles(rolem)
            await user.add_roles(dick)

    @commands.command(
      brief="{Clean a specified amount of messages}", 
      usage="clean <# of Messages>")
    @commands.guild_only()
   # @bot_perms()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clean(self, ctx, count: int):
        """`Deletes a specified amount of messages. (Max 100)`"""
        await ctx.message.delete()
        if not count:
            await ctx.send("Include the amount of messages to delete, you dummy", delete_after=3)
            return
        
        if count>100:
            count = 1
        await ctx.message.channel.purge(limit=count, bulk=True)
            
        await asyncio.sleep(0.5)

        await ctx.send(f"{count} message(s) have been deleted <:trash:734043301187158082>", delete_after=2)

def setup(bot):
    bot.add_cog(Management(bot))
