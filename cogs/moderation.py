
#•----------Modules-----------•#

import discord

from discord.ext.commands import Greedy, command, BucketType, guild_only, cooldown, \
has_permissions, bot_has_permissions, Cog, is_owner, Converter

import asyncio

from asyncio import sleep

import datetime

from datetime import timedelta, datetime

from typing import Optional

import re

#•----------Other Variables-----------•#

time_regex = re.compile("(?:(\d{1,5})(d|days|day|hours|hrs|hour|hr|h|m|minutes|minute|min|mins|seconds|second|sec|secs|s))+?")
#Our dictionary of possible responses
#For when the user gives a time in a command
time_dict = {
  "h": 3600, 
  
  "hours": 3600, 
  
  "hour": 3600, 
  
  "hr": 3600, 
  
  "hrs": 3600, 
  
  "m": 60, 
  
  'minutes': 60, 
  
  'minute': 60, 
  
  'mins': 60, 
  
  "min": 60, 
  
  "days": 86400, 
  
  "day": 86400, 
  
  "d": 86400, 
  
  "s": 1, 
  
  "seconds": 1, 
  
  "sec": 1, 
  
  "secs": 1,  
  
  "second": 1
}

#•----------Class(es)----------•#

#Used to convert the amount of time a user gives
class TimeConverter(Converter):
    async def convert(self, ctx, argument):
        args = argument.lower().split(" ")
        matches = re.findall(time_regex, "".join(args))
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise BadArgument(f"{value} is an invalid time key. Either give days, hours, minutes, or seconds")
            except ValueError:
                raise BadArgument(f"{key} isn't a number")
        return round(time)

class Moderation(Cog, name="Moderation Category"):
  
    """`{Commands for Moderating the Server}`"""
    
    def __init__(self, bot):
        self.bot = bot
        
        #Make a variable to get functions from database
        #Makes stuff a lot easier
        self.db = self.bot.get_cog('Database')
        
        self.gc = self.bot.get_cog('Helpdude')

#•----------Management Commands----------•#
#•----------Configuration Menu-----------•#

    @command(
        brief="{Menu for Server Configuration/Management}", 
        usage="configmenu")
    @guild_only()
    @cooldown(1, 3, BucketType.user)
    @has_permissions(manage_messages=True)
    async def configmenu(self, ctx):
        
        cog = self.gc.get_cog_by_class('Config')
        
        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n*() - Optional\n<> - Required*")
            
        for c in cog.walk_commands():
            
            #Make fields
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", 
                     c.brief, True)]
            
            #Add fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
                    
        e.set_footer(
            text=f"Requested by {ctx.author}", 
            icon_url=ctx.author.avatar_url)
        
        e.timestamp = datetime.utcnow()
        
        await ctx.send(embed=e)
        
#•----------Warn System-----------•#

    @command(
      brief="{Warn a User}", 
      usage="warn <user> (reason)", 
      aliases=['addwarn', 'warnuser'])
    @guild_only()
    @cooldown(1, 3, BucketType.user)
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
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
          
            e.timestamp = datetime.utcnow()
        
            await member.send(embed=e)
            
        except Exception as e:
            pass
        
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
            
        e.timestamp = datetime.utcnow()
        
        e.set_footer(
          text=member, 
          icon_url=member.avatar_url)
        
        await ctx.send(embed=e)
        
    @command(
      brief="{List of Warns a User has", 
      usage="warns (member)", 
      aliases=['warnlist', 'listwarns'])
    @guild_only()
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True, use_external_emojis=True)
    @cooldown(1, 3, BucketType.user)
    async def warns(self, ctx, member: Optional[discord.Member]):
        
        redmark = "<:redmark:738415723172462723>"
        
        #Makes it optional to mention a member
        member = ctx.author if not member else member
        
        #Get the list of warns from database
        warn_list = await self.db.get_warns(member.id, ctx.guild.id)
        
        #Sort warns by number of case
        #warn_sorted = sorted(warn_list, key=lambda wn: wn[3], reverse=True)
        
        #Split the warns into chunks of 5
        warn_chunks = [warn_list[i:i + 5] for i in range(0, len(warn_list), 5)]
        
        # #Start the first page
        # page = 1
        #Max pages we can have
        page_max = len(warn_chunks)
        
        #page variable used for both the embed and for epage indexing
        page = 1
        #list of embeds
        elist = [] #added by Kelsier
    
        #Checks if the user doesn't have any warnings
        if len(warn_list) < 1:
                    err = discord.Embed(
                        color=0x420000, 
                        description=f"{redmark} __*{member.mention} has no warns to display*__")
                    await ctx.send(embed=err)
                    return
        else:
            #Iterate through our chunks
            for chunk in warn_chunks:
                #list of warn fields
                wfields = [] #added by Kelsier

                #Iterate through the list of lists
                #For easier access
                for warn in chunk:
                    #data for embed
                    uid = warn[0]
                    modid = self.bot.get_user(id=warn[1])
                    wreason = warn[2]
                    wcase = warn[3]
                      
                    #Adds a list to the list 'wfields' containing the field data for the current warn
                    wfields.append((
                            f"⚠️ Warn Case **#{wcase}**", 
                        
                            f"\n**  • Mod:** {modid}" +
                            f"\n**  • Reason:** {wreason}", 
                        
                        True))
                          
                #Make an embed for each chunk
                e = discord.Embed(
                    description=f"__*{member.mention}'s Warns -> **{{{len(warn_list)}}}** Total*__")
                
                e.set_thumbnail(
                    url=member.avatar_url)
                
                e.set_footer(
                    text=f"{member}'s ID -> {member.id}")

                e.set_author(
                    name=f"Page {page}/{page_max}")

                #Define fields as the list of fields
                #We have up above
                fields = wfields

                #Add the fields
                for n, v, i in wfields:
                    e.add_field(
                        name=n, 
                        value=v, 
                        inline=i)
                        
                #Connect and store this embed
                #To a certain page
                elist.append(e)
                
                #Add to the current page count
                page += 1
            #Default pages to page 1   
            page = 1
        
            #Send the embed using the page variable
            #To navigate to the correct index within elist
            m = await ctx.send(embed=elist[page-1])
            
            react = ['⬅️', '➡️']
            
            for reaction in react: 
                await m.add_reaction(reaction)

        #Used to make sure only author can trigger reactions
        #And check for the right emojis
        def creact(reaction, user):
            return user == ctx.author and reaction.message.id == m.id and str(reaction.emoji) in ['⬅️', '➡️']

        #Create a while loop so we can..
        #React as many times as we want
        while True:
            try:

                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=creact)
                
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await m.clear_reactions()
                await m.edit(embed=err)
                break
            
            else:
                #Check if the user tried to go forward
                #When on the last page
                if str(reaction.emoji) == "➡️" and page != page_max:
                    await m.remove_reaction(reaction, user)

                    page += 1

                    await m.edit(embed=elist[page-1]) #added by Kelsier

                #Used to check if user tried to go back
                #When on the first page
                elif str(reaction.emoji) =='⬅️' and page > 1:
                    await m.remove_reaction(reaction, user)
                    
                    page -= 1

                    await m.edit(embed=elist[page-1]) #added by Kelsier

                else:
                    await m.remove_reaction(reaction, user)
    
    @command(
        brief="{Delete a Specific Warn}", 
        usage="delwarn <number_of_warn_case>", 
        aliases=['deletewarn', 'dwarn'])
    @guild_only()
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True, use_external_emojis=True)
    @cooldown(1, 3, BucketType.user)
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
            e.timestamp = datetime.utcnow()
            
            await m.edit(embed=ed)
        
    @command(
        brief="{Clear all Warns for a User}", 
        usage="clearwarns <user>", 
        aliases=['clearwrn', 'clearwrns'])
    @guild_only()
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True, use_external_emojis=True)
    @cooldown(1, 3, BucketType.user)
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
    
    @command(
        brief="{Mutes Member(s)",
        usage='mute <member(s) (time)', 
        aliases=['addmute', 'muteuser'])
    @guild_only()
    @cooldown(1, 5, BucketType.user)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Greedy[discord.Member], *, time: TimeConverter=None):
        
        redmark = "<:redmark:738415723172462723>"
        
        #If no members are give 
        if not len(member):
            e = discord.Embed(
                description=f"{redmark} __*{ctx.author.mention}, you have to give a member(s) to mute*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
        
        #Get the muted role
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        #If the mute role doesn't exist in the server
        if not mute_role:
            e = discord.Embed(
                description=f"{redmark} __*Couldn't find a [Muted Role](https://echo-bot.fandom.com/wiki/Setting_up_the_muted_role)", 
                color=0x420000)
            await ctx.send(embed=e)
            return
        
        #Empty list of members for us to to store
        #To unmute later on
        unmutes = []
        
        for mem in member:
            #Check if the member(s) aren't muted already
            if not mute_role in mem.roles:
                #Check if the bot has the right permissions
                #To perform the mute
                if ctx.guild.me.top_role.position > mem.top_role.position:
                    
                    #Store the role ids
                    role_ids = ",".join([str(r.id) for r in mem.roles])
                    #If an endtime was given
                    #Store it, else None
                    endtime = datetime.utcnow() + timedelta(seconds=time) if time else None
                    
                    #Use the function for adding the mute
                    #And storing the member's id, roles, and endtime (if given)
                    await self.db.add_mute(mem.id, role_ids, getattr(endtime, "isoformat", lambda: None)(), ctx.guild.id)
                    
                    #Edit the user's roles
                    await mem.edit(roles=[mute_role])
                    
                    tm = f'{time:,}' if time else 'Indefinite'
                    
                    try:
                        e = discord.Embed(
                            description=f"**You've been muted in {ctx.guild}!**", 
                            timestamp=datetime.utcnow(),  
                            color=0x420000)
                        
                        e.set_author(
                            name=f"Duration -> {tm}")
                        
                        e.set_footer(
                            text=f"Muted by {ctx.author}")
                        
                        e.set_thumbnail(
                            url=ctx.guild.icon_url)
                        
                        await mem.send(embed=e)
                    
                    except Exception:
                        pass
                        
                    #Make our embed
                    e = discord.Embed(
                        description=f"🤐 **{mem.mention} has been muted!**", 
                        color=0x420000, 
                        timestamp=datetime.utcnow())
                    
                    e.set_author(
                        name=f'Duration -> {tm}')

                    #Send the embed
                    await ctx.send(embed=e)
                    
                    #If a time is given
                    #Append the members
                    #To the list of unmutes
                    if time:
                        unmutes.append(mem)
                
                #If the bot doesn't have the right perms
                else:
                    e = discord.Embed(
                        description=f"{redmark} __*{mem.mention} couldn't be muted due to my permission/role hierarchy*__", 
                        color=0x420000)
                    await ctx.send(embed=e)
                    return
            #If the member's already muted
            else:
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention} is already muted!*__", 
                    color=0x420000)
                await ctx.send(embed=e)
                return

        #If a time is given
        #Wait for that amount of time and
        #Then unmute after that time passes
        if len(unmutes):
            await asyncio.sleep(time)
            await self.unmute_mem(ctx, member)
    
    #Method used to unmute members
    async def unmute_mem(self, ctx, member, *, reason="Mute Time Expired"):
        
        #Get the muted role in a server
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        #If a mute role doesn't exist
        if not mute_role:
            return
        
        for mem in member:
            #If the member has the mute role
            if mute_role in mem.roles:
                #Get the roles from the member
                role_ids = await self.db.get_mutes(mem.id, ctx.guild.id)

                roles = [ctx.guild.get_role(int(_id)) for _id in role_ids[0].split(",") if role_ids]
                
                #Unmute the member(s)
                #Deleting them from the database
                await self.db.un_mute(mem.id)
                
                #Edit the member's roles
                #With their old roles
                await mem.edit(roles=roles)
                
                try:
                    e = discord.Embed(
                        description=f"**You've been Unmuted in {ctx.guild}!**",
                        timestamp=datetime.utcnow())
                    
                    e.set_thumbnail(
                        url=ctx.guild.icon_url)
                    
                    e.set_author(
                        name=f"Unmuted by {ctx.author}\nReason -> {reason}")
                    
                    await mem.send(embed=e)
                  
                except Exception:
                    pass
                
                #Make embed
                e = discord.Embed(
                    description=f"**{mem.mention} has been Unmuted!**", 
                    timestamp=datetime.utcnow(), 
                    color=0x420000)
                
                e.set_author(
                    name=f"Reason -> {reason}")

                await ctx.send(embed=e)
            
            else:
                e = discord.Embed(
                    description=f"{redmark} __*{mem.mention} hasn't been muted*__", 
                    color=0x420000)
                return await ctx.send(embed=e)
    
    @command(
        brief="{Unmute Member(s)", 
        usage="unmute <member(s)>")
    @guild_only()
    @has_permissions(manage_roles=True, kick_members=True)
    @bot_has_permissions(manage_roles=True)
    @cooldown(1, 5, BucketType.user)
    async def unmute(self, ctx, member: Greedy[discord.Member], *, reason: Optional[str]="No reason provided"):
        
        redmark = "<:redmark:738415723172462723>"
        
        #If a member isn't given
        if not len(member):
            r = discord.Embed(
                description=f"{redmark} __*{ctx.author.mention}, you have to give 1 or more members to unmute*__", 
                color=0x420000)
            return await ctx.send(embed=r)

        #Use the function from above to unmute
        #The user
        await self.unmute_mem(ctx, member, reason=reason)
        
    @command(
      brief="{Kicks a User from the Guild}", 
      usage="kick <user> (reason_message)")
    @guild_only()
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @cooldown(1, 3, BucketType.user)
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

        e.set_footer(
            text=f'Member: {member.name}\nID: {member.id}')

        e.timestamp = datetime.utcnow()

        e.set_thumbnail(
            url=member.avatar_url)

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

    @command(
      brief="{Bans a User from the Guild}", 
      usage="ban <user> (reason_message)")
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @guild_only()
    @cooldown(1, 3, BucketType.user)
    async def ban(self, ctx, user : discord.Member, *, reason=None):

        if ctx.author == user:
            await ctx.send("You cannot ban yourself.")
            return

        if reason is None:
            await ctx.send("You gotta give a reason for banning this member")
            return

        #Try to send a message to the user
        try:
            e = discord.Embed(
                description=f"__*You've been banned from `{ctx.guild.name}`\n\nReason: {reason}", 
                color=0x420000)
              
            e.timestamp = datetime.utcnow()
              
            await user.send(embed=e)
        except Exception:
            pass

        #Banning the user
        await user.ban()
            
        embed = discord.Embed(
            title=f'Banned {user.name}', 
            description=f'{user.mention} has been banned', 
            color=0x420000)
            
        embed.set_thumbnail(
            url=user.avatar_url)
            
        embed.timestamp = datetime.utcnow()
            
        await ctx.send(embed=embed)

    @command(
      brief="{Unbans a User}", 
      usage="unban <user#1234>")
    @guild_only()
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
      
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
    
    @command(
        brief="{Clean a Specified Amount of Messages}", 
        usage="clean <number>", 
        aliases=['purge', 'prune', 'sweep'])
    @guild_only()
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def clean(self, ctx, count: int):
        
        redmark = "<:redmark:738415723172462723>"
        
        await ctx.message.delete()
        
        #If a number isn't given
        if not count:
            e = discord.Embed(
                description=f"{redmark} __*You have to give a number of messages to delete*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
        
        #If the number is over 100
        if count > 100:
            await ctx.send("You can only delete Max 100 Messages")
            return
         
        #If the number is less than 100
        #Delete
        if count < 100:
            count = 1
            
        await ctx.message.channel.purge(limit=count, bulk=True)
            
        await asyncio.sleep(0.5)

        await ctx.send(f"{count} message(s) have been deleted <:trash:734043301187158082>", delete_after=2)

#•----------Setup/Add this Cog----------•#
def setup(bot):
    bot.add_cog(Moderation(bot))
