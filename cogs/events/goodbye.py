
#•----------Modules----------•#

import discord

from discord.ext.commands import command, guild_only, bot_has_permissions, has_permissions, Cog, group

from datetime import datetime

import aiosqlite

import asyncio

#•----------Class----------•#

class Goodbye(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.db = self.bot.get_cog('Database')
        
#•----------Commands----------•#
    
    #Making the subcommand
    @group(
        invoke_without_command=True, 
        brief="{The Goodbye Menu what else?}", 
        usage="goodbye")
    @guild_only()
    async def goodbye(self, ctx):
      
        #Get this cog
        cog = self.bot.get_cog('Goodbye')
      
        #Get a list of commands/subcommands
        command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]

        #Make embed
        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_", 
            description="\n\n".join(command_desc))
        
        #Make fields
        fields = [
                  ("**Optional Arguments for Setting Text**", 
                  "\n{user} - user#1234)" +
                  "\n{mention} - Mentions the new member" +
                  "\n{members} - Shows the total amount of numbers" +
                  "\n{guild} - Name of Server", False)]
        
        #Add fields      
        for name, val, inl in fields:
            e.add_field(
                name=name, 
                value=val, 
                inline=inl)
            
        e.set_thumbnail(
            url=ctx.author.avatar_url)

        e.timestamp = datetime.utcnow()

        await ctx.send(embed=e)

    @goodbye.command(
      brief="{Change the Channel to Send Goodbye Messages To}", 
      usage="goodbye channel <#channel>"
    )
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def channel(self, ctx, channel: discord.TextChannel):

      try:
          
          #Call the welcome_channel function
          #And save arguments to database
          await self.db.goodbye_channel(ctx.guild.id, channel.id)
          
          #Make and send embed
          e = discord.Embed(
              description=f"**Goodbye Channel has been set to {channel.mention}**")
          
          e.timestamp = datetime.utcnow()
        
          await ctx.send(embed=e)
        
      except Exception as b:
        print(b)

    @goodbye.command(
      brief="{Change the goodbye message (There is also a default)}", 
      usage="goodbye text <new_text_here>", 
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
        
        #Call the function from database
        #And save arguments
        await self.db.goodbye_text(ctx.guild.id, text)

        #Make and send embed
        e = discord.Embed(
          title="**Goodbye Message Set**", 
          description=f"**New Message:** {text}", 
          color=discord.Color.dark_green()
        )

        e.timestamp = datetime.utcnow()

        await ctx.send(embed=e)
        
    @goodbye.command(
        brief="{Check the Current Goodbye Message}", 
        usage="goodbye current", 
        aliases=['currentmsg', 'currenttext', 
                 'currentext', 'currentmessage'])
    @guild_only()
    @has_permissions(manage_channels=True)
    @bot_has_permissions(manage_channels=True)
    async def current(self, ctx):
        
        #Get the current text
        #Using a function from the database
        the_text = await self.db.get_g_text(ctx.guild.id)
        print(the_text)
        
        #If there is no message set in db
        #Show the default
        if the_text is None:
            #Make embed
            e = discord.Embed(
                title="**Default Message**", 
                description="**{mention} just left {guild}. Sorry to see you go!\nMember Count: {members} Members**")
                
            e.timestamp = datetime.utcnow()
        
        #If there IS a message set in db
        #Show that
        if the_text is not None:
            #Make embed
            e = discord.Embed(
                title="**Current Goodbye Message**", 
                description=f"**Message:** {str(the_text)}")
            
            e.timestamp = datetime.utcnow()
            
        
        #Send either of the embeds
        await ctx.send(embed=e)
        
    @goodbye.command(
        brief="{Delete Your Custom Goodbye Message}", 
        usage="rtext", 
        aliases=['removemsg', 'removemessage', 'removetext'])
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True, use_external_emojis=True)
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
            
        #Get the message that user set
        get_db_msg = await self.db.get_g_text(ctx.guild.id)
        print(get_db_msg)
        
        #If there isn't a set message
        if not get_db_msg:
            await ctx.send("There is nothing to remove")
            return
        
        #If there is a set message
        if get_db_msg:

            e = discord.Embed(
                description="⚠️ **Are you sure you want to delete your goodbye message?**")
                
            fields = [("\200", 
                      f"**React With Either: {green_mark} or {red_mark} to Confirm**", 
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
                    await self.db.remove_g_text(ctx.guild.id)
                    
                    e = discord.Embed(
                        description=f"**Deleting Goodbye Message...**")
                
                    await m.edit(embed=e)
                    
                    await asyncio.sleep(1)
                    
                    #New embed to edit the previous
                    edit = discord.Embed(
                        color=0x0F4707, 
                        description=f"**{green_mark} Successfully Deleted Goodbye Message: {str(get_db_msg)}**")
                        
                    #Edit the previous embed
                    await m.edit(embed=edit)
                
                #If the user reacts with an X
                elif str(reaction.emoji) == red_mark:
                    await m.remove_reaction(red_mark, ctx.author)
                    
                    et = discord.Embed(
                        description=f"{red_mark} Custom Message won't be Deleted")
                    et.set_footer(
                        text=ctx.author)
                    et.timestamp = datetime.utcnow()
                    
                    et.set_thumbnail(
                        url=ctx.author.avatar_url)
                    
                    await m.edit(embed=et)
                    
                    return

#•----------Event----------•#

    #Saying goodbye to Members
    @Cog.listener()
    async def on_member_remove(self, member):

      #Check if there's a channel set
      check_channel = await (await self.db.execute("SELECT channel_id FROM goodbye WHERE guild_id = ?", member.guild.id)).fetchone()
      print(check_channel)

      #If there isn't a channel set
      if check_channel is None:
        return

      #If there is a channel set
      elif check_channel is not None:

        #Check if there's a message set
        check_text = await (await self.db.execute("SELECT msg FROM goodbye WHERE guild_id = ?", member.guild.id)).fetchone()
        print(check_text)

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
          colour=discord.Colour.dark_green(), 
          description=str(check_text[0]).format(members=members, mention=mention, user=user, guild=guild))

        e.set_thumbnail(
            url=f"{member.avatar_url}")

        e.set_author(
            name=f"Goodbye {member.name}", 
            icon_url=f"{member.avatar_url}")

        e.set_footer(
            text=f"{member} Left {member.guild}", 
            icon_url=f"{member.guild.icon_url}")

        e.timestamp = datetime.utcnow()

        #IF there is no message set
        #Use a default
        if check_text is None:
          
          e = discord.Embed(
              colour=discord.Colour.dark_green(), 
              description=f"**{member.mention} just left {member.guild}. Sorry to see you go!**\n\n**Member Count: {len(list(member.guild.members))} Members**")

          e.set_thumbnail(
              url=f"{member.avatar_url}")

          e.set_author(name=f"Goodbye {member.name}", icon_url=f"{member.avatar_url}")

          e.set_footer(
              text=f"{member} Left {member.guild}", 
              icon_url=f"{member.guild.icon_url}")

          e.timestamp = datetime.datetime.utcnow()
          
        #Send to the channel the user set
        channel = self.bot.get_channel(id=check_channel[0])

        await channel.send(embed=e)
        
      await self.db.commit()
      await self.db.close()

def setup(bot):
    bot.add_cog(Goodbye(bot))
