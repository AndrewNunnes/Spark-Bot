import discord
from discord.ext import commands
import asyncio
from asyncio import sleep
import datetime
#from cogs.help_command import get_cog_by_class
#from cogs.role import bot_perms


import cogs._json

# This prevents staff members from being punished 
class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
        permission = argument.guild_permissions.manage_messages # can change into any permission
        if not permission: # checks if user has the permission
            return argument # returns user object
        else:
            raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member

## Converters

def can_execute_action(ctx, user, target):
    return user.id == ctx.bot.owner_id or \
           user == ctx.guild.owner or \
           user.top_role > target.top_role

class MemberNotFound(Exception):
    pass

async def resolve_member(guild, member_id):
    member = guild.get_member(member_id)
    if member is None:
        if guild.chunked:
            raise MemberNotFound()
        try:
            member = await guild.fetch_member(member_id)
        except discord.NotFound:
            raise MemberNotFound() from None
    return member

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                member_id = int(argument, base=10)
                m = await resolve_member(ctx.guild, member_id)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
            except MemberNotFound:
                # hackban case
                return type('_Hackban', (), {'id': member_id, '__str__': lambda s: f'Member ID {s.id}'})()

        if not can_execute_action(ctx, ctx.author, m):
            raise commands.BadArgument('You cannot do this action on this user due to role hierarchy.')
        return m

class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.isdigit():
            member_id = int(argument, base=10)
            try:
                return await ctx.guild.fetch_ban(discord.Object(id=member_id))
            except discord.NotFound:
                raise commands.BadArgument('This member has not been banned before.') from None

        ban_list = await ctx.guild.bans()
        entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)

        if entity is None:
            raise commands.BadArgument('This member has not been banned before.')
        return entity

class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = f'{ctx.author} (ID: {ctx.author.id}): {argument}'

        if len(ret) > 512:
            reason_max = 512 - len(ret) + len(argument)
            raise commands.BadArgument(f'Reason is too long ({len(argument)}/{reason_max})')
        return ret

def safe_reason_append(base, to_append):
    appended = base + f'({to_append})'
    if len(appended) > 512:
        return base
    return appended

class Management(commands.Cog):
  
    """⚠️ `{Commands for Moderating the Server}`"""
    def __init__(self,bot):
        self.bot = bot

    @commands.command(
        brief="{Menu for ModLogs}", 
        usage="modlogs", 
        aliases=['logmenu']
    )
    @commands.guild_only()
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def logsmenu(self, ctx):

        cog = self.bot.get_cog('Logging')
        command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            description="\n\n".join(command_desc), 
            color=0x420000)
            
        e.timestamp = datetime.datetime.utcnow()
        
        await ctx.send(embed=e)

    @commands.command(
      brief="{Menu for Role Management}", 
      usage="role")
    @commands.guild_only()
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def role(self, ctx):
      
      #cog = self.get_cog_by_class('Role')
      cog = self.bot.get_cog('Role Management')
      command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]
      
      e = discord.Embed(
        title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
        description="\n\n".join(command_desc), 
        color=0x4D4119)
        
      e.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=e)
      
    @commands.command(
      brief="{Menu for Managing Categories}", 
      usage="categorymenu")
    @commands.guild_only()
    async def categorymenu(self, ctx):
      cog = self.bot.get_cog('Category')
      command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n\n• {c.brief}" for c in cog.walk_commands()]
      
      e = discord.Embed(
        title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
        description="\n\n".join(command_desc), 
        color=0x6B767B)
        
      e.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=e)
      
    @commands.command(
      brief="{Menu for Managing Channels}", 
      usage="channelmenu")
    @commands.guild_only()
    async def channelmenu(self, ctx):
      
      cog = self.bot.get_cog('Channels')
      command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n\n• {c.brief}" for c in cog.walk_commands()]
      
      e = discord.Embed(
        title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
        description="\n\n".join(command_desc), 
        color=0x6B767B)
        
      e.timestamp = datetime.datetime.utcnow()
      
      await ctx.send(embed=e)
      
    @commands.command(
      brief="{Change the Bot's Prefix}", 
      usage="prefix <new_prefix>")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    #@bot_perms()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, *, pre='!'):
      """
      Sets a custom prefix
      """
      data = cogs._json.read_json('prefixes')
      data[str(ctx.message.guild.id)] = pre
      cogs._json.write_json(data, 'prefixes')
      await ctx.send(f"The server prefix has been set to `{pre}`. Use `{pre}prefix <newprefix>` to change it again")
  
    @commands.command(
      brief="{Kicks a User from the Guild}", 
      usage="kick <user> (reason_message)")
    @commands.guild_only()
   # @bot_perms()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        print("Function called")
        #Checking if the user tries to 
        #Kick themselves
        if ctx.author == member:
            await ctx.send("You cannot kick yourself.")
            return
        if reason is None:
            await ctx.send("You gotta give a reason to kick this member")
            return
        try:
            #Sending the member this message
            await member.send(f'You\'ve been kicked from `{ctx.guild.name}` for `{reason}`')
            print("This sends")
        except Exception as e:
            pass

        #Kicking the member
        await member.kick()
        print("kicks the member")

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
      brief="{Mute a User} [NOT DONE]", 
      usage="mute <user> <time>")
    @commands.guild_only()
   # @bot_perms()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def mute(self, ctx, user : discord.Member, time: int):
        """`Prevents a user from speaking for a specified amount of time`"""
        if ctx.author == user:
            await ctx.send("You cannot mute yourself.")
        else:
            rolem = discord.utils.get(ctx.message.guild.roles, name='Muted')
            dick = discord.utils.get(ctx.message.guild.roles, name = 'Verified Member')
            if rolem is None:
                embed=discord.Embed(title="Muted role", url="http://echo-bot.wikia.com/wiki/Setting_up_the_muted_role", description="The mute command requires a role named 'Muted'.", color=discord.Color.dark_red())
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.set_footer(text="Without this role, the command will not work.")
                await ctx.send(embed=embed)
            elif rolem not in user.roles:
                embed = discord.Embed(title=f'User {user.name} has been successfully muted for {time}s.', color=discord.Color.dark_red())
                embed.add_field(name="Shhh!", value=":zipper_mouth:")
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
                await user.add_roles(rolem)
                await user.remove_roles(dick)
                await sleep(time)
                if rolem in user.roles:
                    try:
                        await user.remove_roles(rolem)
                        await user.add_roles(dick)
                        embed = discord.Embed(title=f'User {user.name} has been automatically unmuted.', color=discord.Color.dark_green())
                        embed.add_field(name="Welcome back!", value=":open_mouth:")
                        embed.set_thumbnail(url=user.avatar_url)
                        await ctx.send(embed=embed)
                    except Exception:
                        print(f'User {user.name} could not be unmuted!')
            else:
                await ctx.send(f'User {user.mention} is already muted.')

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

        await ctx.send(f"{count} message(s) have been deleted ðŸ—‘", delete_after=2)

def setup(bot):
    bot.add_cog(Management(bot))
