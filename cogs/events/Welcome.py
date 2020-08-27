
#•----------Modules----------•#

import discord

from discord.ext.commands import command, guild_only, bot_has_permissions, has_permissions, Cog, group

from datetime import datetime

import aiosqlite

import asyncio

#•----------Class----------•#

class Welcome(Cog):
  
    """`Commands to Setup Welcome Messages`"""
    
    def __init__(self, bot):
        self.bot = bot
        
        self.db = self.bot.get_cog('Database')
        
        self.gc = self.bot.get_cog('Helpdude')
        
#•----------Commands----------•#
    
    #Making the subcommand
    @group(
        invoke_without_command=True, 
        brief="{The Welcome Menu what else?}", 
        usage="welcome")
    @guild_only()
    @bot_has_permissions(use_external_emojis=True)
    async def welcome(self, ctx):
      
        #Get this cog
        cog = self.gc.get_cog_by_class('Welcome')
        

        desc = ["**Optional Arguments for Setting Text**" + 
                "\n__*Supports Markdown <:greenmark:738415677827973152>*__" +
                "\n\n__*To make new lines press `Enter/Return`*__" +
                "\n\n•-------------------•" +
                "\n\n{user} - user#1234)" +
                "\n{mention} - Mentions the new member" +
                "\n{members} - Shows the total amount of members" +
                "\n{guild} - Name of Server"]
        
        #Make embed
        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n*() - Optional\n<> - Required*", 
            description="".join(desc))
                  
        for c in cog.walk_commands():
            #Make the fields
            fields = [
                      (f"• **{c.name} :** `{ctx.prefix}{c.usage}`", c.brief, True)]
              
            #Add the fields
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)

        e.set_thumbnail(
            url=ctx.author.avatar_url)

        e.timestamp = datetime.utcnow()

        await ctx.send(embed=e)

    @welcome.command(
      brief="{Change the Channel to Send Welcome Messages To}", 
      usage="welcome channel <#channel>"
    )
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def channel(self, ctx, channel: discord.TextChannel):

      try:
          
          #Call the welcome_channel function
          #And save arguments to database
          await self.db.welcome_channel(ctx.guild.id, channel.id)
          
          #Make and send embed
          e = discord.Embed(
              description=f"**Welcome Channel has been set to {channel.mention}**")
          
          e.timestamp = datetime.utcnow()
        
          await ctx.send(embed=e)
        
      except Exception as b:
        print(b)
        
    @welcome.command(
        brief="{Check the current channel set}", 
        usage="welcome currentchann", 
        aliases=['currentchannel', 'cc', 
                'ccurrent', 'currentc'])
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def currentchann(self, ctx):
      
        #Make the function from database.py
        #A var to check if its None for later 
        check_channel = await self.db.get_welcome_channel(ctx.guild.id)

        #If there's no channel set
        if check_channel[0] is None:
          
            await ctx.send("There is no channel set")
            return
        
        #If there is a channel set
        if check_channel:
            
            e = discord.Embed(
                description=f"**Current channel is <#{check_channel[0]}>**")
                
            e.timestamp = datetime.utcnow()
        
        #Send either of the embeds
        await ctx.send(embed=e)

    @welcome.command(
      brief="{Change the welcome message (There is also a default)}", 
      usage="welcome text <new_text_here>", 
      aliases=['message', 'msg'])
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def text(self, ctx, *, text):
      
        #Check if the text user sets
        #Is too high
        if len(text) > 350:
          await ctx.send("Text has a limit of `350 Characters`")
          return
        
        #Check if there's a channel set first
        check_channel = await self.db.get_welcome_channel(ctx.guild.id)
        
        #If there isn't a channel
        if check_channel[0] is None:
            
            await ctx.send("Welcome messages are turned off")
            return
          
        #If there is a channel set
        if check_channel is not None:
          
            #Call the function from database
            #And save arguments
            await self.db.welcome_text(ctx.guild.id, text)
        
            #Make and send embed
            e = discord.Embed(
                title="**Welcome Message Set**",
                description=f"**New Message:** {text}")
                
            e.timestamp = datetime.utcnow()
        
            await ctx.send(embed=e)

    @welcome.command(
        brief="{Check the Current Welcome Message}", 
        usage="welcome currentmsg", 
        aliases=['currenttext', 
                 'currentext', 'currentmessage', 'cmsg', 'ctext', 'cmessage'])
    @guild_only()
    @has_permissions(manage_channels=True)
    @bot_has_permissions(manage_channels=True)
    async def currentmsg(self, ctx):
      
        check_chann = await self.db.get_welcome_channel(ctx.guild.id)
        
        #If there isn't a channel set
        if check_chann[0] is None:
            
            await ctx.send("Welcome messages are turned off")
            return

        #If there is a channel set
        if check_chann is not None:

            #Get the current text
            #Using a function from the database
            the_text = await self.db.get_w_text(ctx.guild.id)

            #If there is no message set in db
            #Show the default
            if the_text is None:
            
                #Make embed
                e = discord.Embed(
                    title="**Default Welcome Message**", 
                    description="**{mention} just left {guild}. Sorry to see you go!**\n__*Member Count: {members} Members*__")
                
                e.timestamp = datetime.utcnow()
        
            #If there IS a message set in db
            #Show that
            if the_text is not None:
                #Make embed
                e = discord.Embed(
                    title="**Current Welcome Message**", 
                    description=f"**Message:** {str(the_text)}")
            
                e.timestamp = datetime.utcnow()

            #Send either of the embeds
            await ctx.send(embed=e)

    @welcome.command(
        brief="{Delete Your Set Welcome Channel}", 
        usage="welcome rtext", 
        aliases=['removechannel', 'removechann', 'rch', 'rc'])
    @guild_only()
    @bot_has_permissions(manage_channels=True, use_external_emojis=True)
    @has_permissions(manage_channels=True)
    async def rchannel(self, ctx):
      
        #Reactions for user to choose
        custom_emojis = ["<:greenmark:738415677827973152>", "<:redmark:738415723172462723>"]
        
        #Just defining custom emojis
        #To make it easier for me
        green_mark = "<:greenmark:738415677827973152>"
        
        red_mark = "<:redmark:738415723172462723>"
        
        #Custom check to check
        #For the user's reaction
        def check_react(reaction, user):
            return user == ctx.author and str(reaction.emoji) in custom_emojis
            
        #Get the message that user set
        get_channel = await self.db.get_welcome_channel(ctx.guild.id)

        #If there isn't a set message
        if get_channel[0] is None:
            await ctx.send("There is no channel to remove")
            return
        
        #If there is a set message
        if get_channel is not None:

            e = discord.Embed(
                description="⚠️ **Are you sure you want to delete your Welcome channel? Deleting will also turn off Welcome messages**")
                
            fields = [("\200", 
                      f"__*React With Either: {green_mark} or {red_mark} to Confirm*__", 
                      False)]
            
            for name, val, inl in fields:
                e.add_field(
                    name=name, 
                    value=val, 
                    inline=inl)
            
            #Make this a variable
            #To add the reactions
            m = await ctx.send(embed=e)
            
            #Add reactions
            await m.add_reaction(green_mark)
            await m.add_reaction(red_mark)

            try:
                #Wait for the user to react
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check_react)
            
            #If the user takes too long to say yes or no
            except asyncio.TimeoutError:
              
                e = discord.Embed(
                    color=0x420000, 
                    description="⚠️ **You took too long to confirm**")
                    
                e.set_thumbnail(
                    url=ctx.author.avatar_url)
                    
                e.set_footer(
                    text=ctx.author)
                e.timestamp = datetime.utcnow()
                
                await m.edit(embed=e)
                #Remove the reactions
                await m.clear_reactions()
                
                return
              
            else:
                
                #If the user reacts with
                #A check mark
                if str(reaction.emoji) == green_mark:
                    await m.remove_reaction(green_mark, ctx.author)
                    
                    #Function to remove the channel from database
                    await self.db.remove_w_channel(ctx.guild.id)
                    
                    #New embeds to edit the original
                    e = discord.Embed(
                        description=f"**Deleting Channel and Turning off Welcome Messages...**")
                
                    await m.edit(embed=e)
                    
                    await asyncio.sleep(1)
                    
                    edit = discord.Embed(
                        color=0x0F4707, 
                        description=f"**{green_mark} Successfully Deleted <#{get_channel}> and Turned off Welcome Messages**")
                        
                    #Edit the previous embed
                    await m.edit(embed=edit)
                    await m.clear_reactions()
                
                #If the user reacts with an X
                elif str(reaction.emoji) == red_mark:
                    await m.remove_reaction(red_mark, ctx.author)
                    
                    #Make a new embed
                    #To edit the original
                    et = discord.Embed(
                        description=f"**{red_mark} Channel Won't be Deleted and Welcome Messages are Still Enabled**")
                    et.set_footer(
                        text=ctx.author)
                    et.timestamp = datetime.utcnow()
                    
                    et.set_thumbnail(
                        url=ctx.author.avatar_url)
                    
                    await m.edit(embed=et)
                    await m.clear_reactions()
                    
                    return
        
    @welcome.command(
        brief="{Delete Your Custom Welcome Message}", 
        usage="welcome rtext", 
        aliases=['removemsg', 'removemessage', 'removetext', 'rmsg', 'rmessage'])
    @guild_only()
    @bot_has_permissions(manage_channels=True, use_external_emojis=True)
    @has_permissions(manage_channels=True)
    async def rtext(self, ctx):
      
        #Reactions for user to choose
        custom_emojis = ["<:greenmark:738415677827973152>", "<:redmark:738415723172462723>"]
        
        #Just defining custom emojis
        #To make it easier for me
        green_mark = "<:greenmark:738415677827973152>"
        
        red_mark = "<:redmark:738415723172462723>"
        
        #Custom check to check
        #For the user's reaction
        def check_react(reaction, user):
            return user == ctx.author and str(reaction.emoji) in custom_emojis
            
        checkchannel = await self.db.get_welcome_channel(ctx.guild.id)
        
        if checkchannel is None:
            await ctx.send("Welcome Messages are  Turned off")
            return

        if checkchannel is not None:
            
            #Get the message that user set
            get_db_msg = await self.db.get_w_text(ctx.guild.id)

            #If there isn't a set message
            if not get_db_msg:
                await ctx.send("There is nothing to remove")
                return
        
            #If there is a set message
            if get_db_msg:

                e = discord.Embed(
                    description="⚠️ **Are you sure you want to delete your Welcome message?**")
                
                fields = [("\200", 
                          f"__*React With Either: {green_mark} or {red_mark} to Confirm*__", 
                          False)]
            
                for name, val, inl in fields:
                    e.add_field(
                        name=name, 
                        value=val, 
                        inline=inl)
            
                #Make this a variable
                #To add the reactions
                m = await ctx.send(embed=e)
            
                #Add reactions
                await m.add_reaction(green_mark)
                await m.add_reaction(red_mark)

                try:
                    #Wait for the user to react
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check_react)
            
                #If the user takes too long to say yes or no
                except asyncio.TimeoutError:
              
                    e = discord.Embed(
                        color=0x420000, 
                        description="⚠️ **You took too long to confirm**")
                    
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)
                    
                    e.set_footer(
                        text=ctx.author)
                    e.timestamp = datetime.utcnow()
                
                    await m.edit(embed=e)
                    #Remove the reactions
                    await m.clear_reactions()
                
                    return
              
                else:
                
                    #If the user reacts with
                    #A check mark
                    if str(reaction.emoji) == green_mark:
                        await m.remove_reaction(green_mark, ctx.author)
                    
                        #Function to remove the text from database
                        await self.db.remove_w_text(ctx.guild.id)
                    
                        e = discord.Embed(
                            description=f"**Deleting Welcome Message...**")
                
                        await m.edit(embed=e)
                    
                        await asyncio.sleep(1)
                    
                        #New embed to edit the previous
                        edit = discord.Embed(
                            color=0x0F4707, 
                            description=f"**{green_mark} Successfully Deleted Welcome Message:** {str(get_db_msg)}")
                        
                        #Edit the previous embed
                        await m.edit(embed=edit)
                        await m.clear_reactions()
                
                    #If the user reacts with an X
                    elif str(reaction.emoji) == red_mark:
                        await m.remove_reaction(red_mark, ctx.author)
                    
                        et = discord.Embed(
                            description=f"**{red_mark} Custom Message won't be Deleted**")
                        et.set_footer(
                            text=ctx.author)
                        et.timestamp = datetime.utcnow()
                    
                        et.set_thumbnail(
                            url=ctx.author.avatar_url)
                    
                        await m.edit(embed=et)
                        await m.clear_reactions()
                    
                        return
                  
    @welcome.command(
        brief="{Get a preview of your embed}", 
        usage="welcome preview", 
        aliases=['prv', 'pview', 'pv'])
    @guild_only()
    @has_permissions(manage_channels=True)
    @bot_has_permissions(manage_channels=True)
    async def preview(self, ctx):

      guild = ctx.guild
      
      #Defining member as the author
      member = ctx.author

      #Check if there's a channel set
      check_channel = await self.db.get_welcome_channel(ctx.guild.id)

      #If there isn't a channel set
      if check_channel[0] is None:
          await ctx.send("There's Nothing to Preview if Welcome Messages are Turned Off")
          return

      #If there is a channel set
      elif check_channel is not None:
          
          #Check if there's a message set
          check_text = await self.db.get_w_text(ctx.guild.id)

          #If there is a message set
          #Send that
          if check_text is not None:
            
              #List of optionaal variables
              #For the welcome message
              members = len(list(ctx.guild.members))

              mention = member.mention

              user = member

              guild = ctx.guild

              #Adjust the embed to what the user
              #Set the variables to
              e = discord.Embed(
                  colour=0x0F4707, 
                  description=str(check_text).format(members=members, mention=mention, user=user, guild=guild))

              e.set_thumbnail(
                  url=f"{member.avatar_url}")

              e.set_author(
                  name=f"Welcome {member.name}",
                  icon_url=f"{member.avatar_url}")

              e.set_footer(
                  text=f"{member} Joined {guild}", 
                  icon_url=f"{guild.icon_url}")
              e.timestamp = datetime.utcnow()
              
              #channel = self.bot.get_channel(id=check_channel[0])
              
              #await channel.send(embed=e)

          #IF there is no message set
          #Send a default
          if check_text is None:
            
              e = discord.Embed(
                  colour=0x0F4707, 
                  description=f"**Welcome {member.mention} to {guild}! We hope you enjoy your stay!**\n__*Member Count: {len(list(guild.members))} Members*__")

              e.set_thumbnail(
                  url=f"{member.avatar_url}")

              e.set_author(
                  name=f"Welcome {member.name}", 
                  icon_url=f"{member.avatar_url}")

              e.set_footer(
                  text=f"{member} Joined {ctx.guild}", 
                  icon_url=f"{ctx.guild.icon_url}")

              e.timestamp = datetime.utcnow()
              
          await ctx.send(embed=e)
        

#•----------Event----------•#

    #Saying goodbye to Members
    @Cog.listener()
    async def on_member_join(self, member):

      #Check if there's a channel set
      check_channel = await self.db.get_welcome_channel(member.guild.id)
      
      #If there isn't a channel set
      if check_channel is None:
        return

      #If there is a channel set
      elif check_channel is not None:
          
          #Check if there's a message set
          check_text = await self.db.get_w_text(member.guild.id)

          #If there is a message set
          #Send that
          if check_text is not None:
            
              #List of optionaal variables
              #For the welcome message
              members = len(list(member.guild.members))

              mention = member.mention

              user = member

              guild = member.guild

              gicon = member.guild.icon_url

              micon = member.avatar_url

              #Adjust the embed to what the user
              #Set the variables to
              e = discord.Embed(
                  colour=0x0F4707, 
                  description=str(check_text).format(members=members, mention=mention, user=user, guild=guild))

              e.set_thumbnail(
                  url=f"{member.avatar_url}")

              e.set_author(
                  name=f"Welcome {member.name}",
                  icon_url=f"{member.avatar_url}")

              e.set_footer(
                  text=f"{member} Joined {member.guild}", 
                  icon_url=f"{member.guild.icon_url}")
              e.timestamp = datetime.utcnow()
              
              #channel = self.bot.get_channel(id=check_channel[0])
              
              #await channel.send(embed=e)

          #IF there is no message set
          #Send a default
          if check_text is None:

              e = discord.Embed(
                  colour=0x0F4707, 
                  description=f"**Welcome {member.mention} to {member.guild}! We hope you enjoy your stay!**\n__*Member Count: {len(list(member.guild.members))} Members*__")

              e.set_thumbnail(
                  url=f"{member.avatar_url}")

              e.set_author(
                  name=f"Welcome {member.name}", 
                  icon_url=f"{member.avatar_url}")

              e.set_footer(
                  text=f"{member} Joined {member.guild}", 
                  icon_url=f"{member.guild.icon_url}")

              e.timestamp = datetime.utcnow()
            
          #Send to the channel the user set
          channel = self.bot.get_channel(id=check_channel[0])
                
          await channel.send(embed=e)

    #Sends an embed to show the default prefix
    #When bot joins a guild
    @Cog.listener()
    async def on_guild_join(self, guild):
      
      names = ['comman', 'bot']
      channel = discord.utils.find(
          lambda channel:any(
            map(lambda w: w in channel.name, names)),
            guild.text_channels) #When the bot joins a server, this will check for a bot commands channel to send an embed
      
      #If a bot commands channel doesn't exist
      #It'll look for a general channel
      if not channel: 
        
          newchann = ['gener', 'chat', 'welc', 'memb']
          new = discord.utils.find(
              lambda new:any(
                map(lambda n: n in new.name, newchann)),
                guild.text_channels)
            
          e = discord.Embed(
              description="**What's up everyone! Type in `!help` to see all of my available commands and get started!**\n\n")
              
          e.set_thumbnail(
              url=self.bot.user.avatar_url)
          
          e.timestamp = datetime.utcnow()
        
          await new.send(embed=e)
            
      e = discord.Embed(
          description="**What's up everyone! Type `!help` to see all of my commands and get started!**\n\n")
          
      e.set_thumbnail(
          url=self.bot.user.avatar_url)
      
      e.timestamp = datetime.utcnow()
      
      await channel.send(embed=e)


#Setup the cog   
def setup(bot):
    bot.add_cog(Welcome(bot))
