#•----------Modules----------•#
import discord

from discord.ext.commands import command, Cog, BucketType, guild_only, cooldown, bot_has_permissions, is_owner

import asyncio

import logging

from datetime import datetime

#•----------Logging----------•#

logging.basicConfig(level = logging.INFO)

#•----------Class----------•#

class Helpdude(Cog):
    def __init__(self, bot):
        self.bot = bot
        
#•----------Functions----------•#

    #Function to call when wanting to get a different Cog by it's Class     
    def get_cog_by_class(self, name):
        for cog in self.bot.cogs.values():
            if cog.__class__.__name__ == name:
                return cog

#•----------Commands----------•#
   
    @command()
    @is_owner()
    async def pagehelp(self, ctx):

      info = self.get_cog_by_class('Info')
      
      fun = self.get_cog_by_class('Fun')
      
      e = discord.Embed(
          description="**{Category Index}**")
      
      fields = [
             (f"__*{info.qualified_name}*__", info.description, True), 
             
             (f"__*{fun.qualified_name}*__", fun.description, True)]
             
      for n, v, i in fields:
          e.add_field(
              name=n, 
              value=v, 
              inline=i)
      
      info_commands = [f"**{c.name} :** `{ctx.prefix}{c.usage}`\n{c.brief}" for c in info.get_commands()]
      
      contents = [e, info_commands, "huh", "okay"]
      
      #Max amount of pages
      pages = 4
      #First page
      cur_page = 1
      
      #Store the embed we're sending as a variable
      #For editing and adding reactions
      m = await ctx.send(
          embed=contents[cur_page-1])
      
      await m.add_reaction('⬅️')
      await m.add_reaction('➡️')
      
      #Check to make sure nobody else
      #But the author triggers the reactions
      def author(reaction, user):
          return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']
          
      while True:
          try:
              reaction, user = await self.bot.wait_for('reaction_add', check=author, timeout=60.0)
          
              if str(reaction.emoji) == "➡️" and cur_page != pages:
                  await m.remove_reaction(reaction, user)
                  cur_page += 1
                  
                  e = discord.Embed(
                      description=f"{contents[cur_page-1]}")
                  
                  await m.edit(embed=e)
                  
              elif str(reaction.emoji) == "⬅️" and cur_page > 1:
                  await m.remove_reaction(reaction, user)
                  cur_page -= 1
                  
                  e = discord.Embed(
                      description=f"{contents[cur_page-1]}")
                  await m.edit(embed=e)
              else:
                  await m.remove_reaction(reaction, user)
                  
          except asyncio.TimeoutError:
              await m.edit(content="Took too long")
              break
            
    @command()
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def help(self, ctx, member: discord.Member=None):
        await ctx.message.delete()
        
        member = ctx.author if not member else member
        
        #Gets the Cogs
        info = self.get_cog_by_class('Info')
        
        fun = self.get_cog_by_class('Fun')
        
        giveaway = self.get_cog_by_class('Giveaway')
        
        mod = self.get_cog_by_class('Moderation')
        
        misc = self.get_cog_by_class('Misc')

        owner = self.get_cog_by_class('Owner')
        
        e = discord.Embed(
            description="__**{{Category Index}}**__")
            
        #Make fields 
        fields = [
                  ("**📖 Main Menu**", "{`Shows this Menu}`", True), 
                  
                  (f"📰 **{info.qualified_name}**", info.description, True), 
                  
                  (f"🎪 **{fun.qualified_name}**", fun.description, True), 
                  
                  (f"🎉 **{giveaway.qualified_name}**", giveaway.description, True), 
                  
                  (f"⚙️ **{mod.qualified_name}**", mod.description, True), 
                  
                  (f"🔐 **{owner.qualified_name}**", owner.description, True), 
                  
                  (f"🔗 **{misc.qualified_name}**", misc.description, True), 
                  
                  ("<:trash:734043301187158082> **Cancellation**", 
                  "`Deletes this Embed/Help Message`", True)]
        
        #Add the fields      
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
        
        m = await ctx.send(embed=e)
        
        #Adding the reactions
        reactions = ['📖', '📰', '🎪', '🎉', '⚙️', '🔐', '🔗', '<:trash:734043301187158082>']
        for react in reactions:
          await m.add_reaction(react)
          
        #Check to make sure no other users can click on the reactions
        def checkreact(reaction, user):
            return user == ctx.author and reaction.message.id == m.id and str(reaction.emoji) in ['📖', '📰', '🎪', '🎉', '⚙️', '🔐', '🔗', '<:trash:734043301187158082>']
            
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=75.0, check=checkreact)
            
            #If the User takes too long to react
            except asyncio.TimeoutError:

                alert = f"<:redmark:738415723172462723> __*{ctx.author.mention}, You took too long to React*__\n\n*Help Embed Retracted*"
              
                e = discord.Embed(
                    color=0x420000, 
                    description=alert)
                    
                e.set_thumbnail(
                    url=ctx.author.avatar_url)
                    
                e.set_footer(
                    text=ctx.author)
                
                e.timestamp = datetime.utcnow()
              
                await m.edit(embed=e)
                await m.clear_reactions()
                #Break the loop
                break
                
            #Menus for when they react
            else:

                if str(reaction.emoji) == '🎉':
                    await m.remove_reaction('🎉', member)
                      
                    cog = self.get_cog_by_class('Giveaway')

                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__")
                      
                    for c in cog.get_commands():
                        
                        #Make fields
                        fields = [
                                 (f"• **{c.name} :** `{ctx.prefix}{c.usage}`", 
                                 c.brief, True)]
                           
                        #Add fields      
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)
                                
                    e.set_footer(
                        text=f"Requested by {ctx.author}")

                    e.timestamp = datetime.utcnow()

                    await m.edit(embed=e)

                  
                elif str(reaction.emoji) == '📰':
                    await m.remove_reaction('📰', member)
                    
                    cog = self.get_cog_by_class('Info')

                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__")

                    for c in cog.get_commands():
                        
                        #Make fields
                        fields = [
                                 (f"• **{c.name} :** `{ctx.prefix}{c.usage}`", 
                                 c.brief, True)]
                           
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

                    await m.edit(embed=e)

                    
                elif str(reaction.emoji) == '🎪':
                    await m.remove_reaction('🎪', member)

                    cog = self.get_cog_by_class('Fun')
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__")

                    for c in cog.get_commands():
                        
                        #Make fields
                        fields = [
                                 (f"• **{c.name} :** `{ctx.prefix}{c.usage}`", 
                                 c.brief, True)]
                           
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

                    await m.edit(embed=e)

                #This deletes the embed
                elif str(reaction.emoji) == '<:trash:734043301187158082>':
                    await m.remove_reaction('<:trash:734043301187158082>', member)
                    
                    e = discord.Embed(
                        description="__*Removing this Embed in 5 Seconds...*__", 
                        color=0x420000)
                        
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)
                        
                    e.set_footer(
                        text=ctx.author)
                    
                    e.timestamp = datetime.utcnow()
                    
                    await m.clear_reactions()
                    await m.edit(embed=e, delete_after=5)

                elif str(reaction.emoji) == '⚙️':
                    await m.remove_reaction('⚙️', member)
                    
                    cog = self.get_cog_by_class('Moderation')
                    

                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__")

                    for c in cog.get_commands():
                        
                        #Make fields
                        fields = [
                                 (f"• **{c.name} :** `{ctx.prefix}{c.usage}`", 
                                 c.brief, True)]
                           
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

                    await m.edit(embed=e)

                    
                elif str(reaction.emoji) == '🔐':
                    await m.remove_reaction('🔐', member)
                    
                    cog = self.get_cog_by_class('Owner')

                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__")

                    for c in cog.get_commands():
                        
                        #Make fields
                        fields = [
                                 (f"• **{c.name} :** `{ctx.prefix}{c.usage}`", 
                                 c.brief, True)]
                           
                        #Add fields      
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)
                                
                    e.set_footer(
                        text=f"Requested by {ctx.author}")

                    e.timestamp = datetime.utcnow()

                    await m.edit(embed=e)

                    
                elif str(reaction.emoji) == '🔗':
                    await m.remove_reaction('🔗', member)
                    
                    cog = self.get_cog_by_class('Misc')
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__")

                    for c in cog.get_commands():
                        
                        #Make fields
                        fields = [
                                 (f"• **{c.name} :** `{ctx.prefix}{c.usage}`", 
                                 c.brief, True)]
                           
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

                    await m.edit(embed=e)

                else:
                    if str(reaction.emoji) == '📖':
                        await m.remove_reaction('📖', member)

                        #Gets the Cogs
                        info = self.get_cog_by_class('Info')
        
                        fun = self.get_cog_by_class('Fun')
        
                        giveaway = self.get_cog_by_class('Giveaway')
        
                        mod = self.get_cog_by_class('Moderation')
        
                        misc = self.get_cog_by_class('Misc')

                        owner = self.get_cog_by_class('Owner')
                        
                        #Make embed
                        e = discord.Embed(
                            description="__**{{Category Index}}**__")

                        #Make fields 
                        fields = [
                                  ("**📖 Main Menu**", "{`Shows this Menu}`", True), 

                                  (f"📰 **{info.qualified_name}**", info.description, True), 
                  
                                  (f"🎪 **{fun.qualified_name}**", fun.description, True), 
                                  
                                  (f"🎉 **{giveaway.qualified_name}**", giveaway.description, True), 

                                  (f"⚙️ **{mod.qualified_name}**", mod.description, True), 
                                  
                                  (f"🔐 **{owner.qualified_name}**", owner.description, True), 
                                  
                                  (f"🔗 **{misc.qualified_name}**", misc.description, True), 
                                  
                                  ("<:trash:734043301187158082> Cancellation", 
                                  "`Deletes this Embed/Help Message`", True)]
                        
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
                    
                        await m.edit(embed=e)

    @command()
    @guild_only()
    async def pages(self, ctx):
      
        info = self.get_cog_by_class('Info')
        
        fun = self.get_cog_by_class('Fun')
        
        e = discord.Embed(
            description=f"{info.qualified_name}")
        
        f = discord.Embed(
            description=f"{fun.qualified_name}")
        
        contents = [f"{e}", "This is page 2!", f"{f}", "This is page 4!"]
        pages = 4
        cur_page = 1
        message = await ctx.send(f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds

    @command()
    @guild_only()
    async def testhelp(self, ctx, *cog):

        if not cog:

            embed = discord.Embed(
                color=discord.Color.darker_grey())

            cogs_desc = ''
            for x in self.bot.cogs:
                cogs_desc += ('**{}** - {} '.format(x, self.bot.cogs[x].__doc__)+'\n')
            embed.add_field(name="Categories", value=cogs_desc[0:len(cogs_desc)-1], inline=True)
            await ctx.send(embed=embed)
        else:
            if len(cog) > 1:
                embed = discord.Embed(
                    title="Error Occured", 
                    description="That's way too many cogs", 
                    color=discord.Color.darker_grey()
                )
                await ctx.send(embed=embed)
            else:
                found = False
                for x in self.bot.cogs:
                   for y in cog:
                        if x == y:
                            embed = discord.Embed(color=discord.Color.darker_grey())
                            scog_info = ''
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    scog_info += f'**{c.name}** - {c.help}\n'
                            embed.add_field(name=f'{cog[0]} Module - {self.bot.cogs[cog[0]].__doc__}', value=scog_info)
                            found = True
                if not found:
                    for x in self.bot.cogs:
                        for c in self.bot.get_cog(x).get_commands():

                            if c.name == cog[0]:
                                embed = discord.Embed(color=discord.Color.darker_grey())
                                embed.add_field(name=f'{c.name} - {c.help}', value=f'Proper Syntax:\n`{c.qualified_name} {c.signature}`')

                        found = True
                    if not found:
                        embed = discord.Embed(title="Error Occurred", description='"`+cog[0]+`" doesn\'t even exist', color=discord.Color.darker_grey())
                else:
                    await ctx.send(embed=embed)

#•----------Setup/Add this Cog----------•#
def setup(bot):
    bot.add_cog(Helpdude(bot))
