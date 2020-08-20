import discord
from discord.ext import commands
import asyncio
import logging
import datetime

logging.basicConfig(level = logging.INFO)

class Helpdude(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Function to call when wanting to get a different Cog/Class     
    def get_cog_by_class(self, name):
      for cog in self.bot.cogs.values():
        if cog.__class__.__name__ == name:
          return cog

# The New Help Command

    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        
        member = ctx.author if not member else member
        
        #Gets the Cogs
        gene = self.get_cog_by_class('General')
        
        fun = self.get_cog_by_class('Fun')
        
        giveaway = self.get_cog_by_class('Giveaway')
        
        management = self.get_cog_by_class('Management')
        
        misc = self.get_cog_by_class('Misc')
        
        e = discord.Embed(
            title=f'(Default prefix is `{ctx.prefix}`)',
            description="__**{{Category Index}}**__",
            color=0x232323)
        
        e.add_field(
          name="📖 Main Menu", 
          value="`{Shows this Menu}`", 
          inline=False)
        
        e.add_field(
          name=f"{gene.qualified_name}", 
          value=f"{gene.description}", 
          inline=False)
          
        e.add_field(
          name=f"<:fun:734648757441921124> {fun.qualified_name}", 
          value=f"{fun.description}", 
          inline=False)
          
        e.add_field(
          name=f"{giveaway.qualified_name}", 
          value=f"{giveaway.description}", 
          inline=False)
          
        e.add_field(
          name="📚 Application/Suggestion Category", 
          value="`List of Application/Suggestion Commands`", 
          inline=False)
          
        e.add_field(
          name=f"{management.qualified_name}", 
          value=f"{management.description}", 
          inline=False)
          
        e.add_field(
          name=f"{misc.qualified_name}", 
          value=f"{misc.description}", 
          inline=False)
          
        e.add_field(name="<:trash:734043301187158082> Cancellation", value="`Deletes this Embed/Help Message`", inline=False)
        
        e.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        
        e.set_footer(text="{{Please Remember This Bot Is Not 100% Finished Yet}}")
        
        m = await ctx.send(embed=e)
        
        #Adding the reactions
        reactions = ['📖', '📯', '<:fun:734648757441921124>', '🎉', '📚', '⚠️', '🔗', '<:trash:734043301187158082>']
        for react in reactions:
          await m.add_reaction(react)
          
        #Check to make sure no other users can click on the reactions
        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📖', '📯', '<:fun:734648757441921124>', '🎉', '⚠️','📚', '🔗', '<:trash:734043301187158082>']
            
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=45.0, check=checkreact)
            
            #If the User takes too long to react
            except asyncio.TimeoutError:
                bruh = discord.Embed(color=discord.Color.darker_grey())
                bruh.add_field(name="__**What were you doing?**__", value="You took too long to react with an emoji bruh 🤦🏽")
                bruh.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                await m.edit(embed=bruh)
                
            #Menus for when they react
            else:
                print("Menus show")
                if str(reaction.emoji) == '🎉':
                    await m.remove_reaction('🎉', member)
                      
                    cog = self.get_cog_by_class('Giveaway')
                    command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*_\n_*() - Optional\n<> - Required\n\n__*Your Available Commands*_", 
                      description="\n\n".join(command_desc), 
                      color=0x575409)
                    
                    e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    await m.edit(embed=e)
                    print("Below here")
                  
                elif str(reaction.emoji) == '📯':
                    await m.remove_reaction('📯', member)
                    
                    cog = self.get_cog_by_class('General')
                    command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
                      description="\n\n".join(command_desc), 
                      color=0x232B45)
                      
                    e.timestamp = datetime.datetime.utcnow()

                    e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    await m.edit(embed=e)
                    print("Edits")
                    
                elif str(reaction.emoji) == '<:fun:734648757441921124>':
                    await m.remove_reaction('<:fun:734648757441921124>', member)
                    
                    cog = self.get_cog_by_class('Fun')
                    command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
                      description="\n\n".join(command_desc), 
                      color=0x215522)
                      
                    e.timestamp = datetime.datetime.utcnow()
                    
                    e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    await m.edit(embed=e)
            
                elif str(reaction.emoji) == '📚':
                    await m.remove_reaction('📚', member)
                    embed4 = discord.Embed(title=f'Application/Suggestion Category (Default prefix is `{ctx.prefix}`)', color=0x45193A)

                    embed4.add_field(
                      name="_*applymod {Apply for Mod}*_", 
                      value=f"{{`{ctx.prefix}applymod`}}", 
                      inline=True)
                      
                    embed4.add_field(
                      name="_*suggest {Leave a Suggestion}*_", 
                      value=f"{{`{ctx.prefix}suggest <suggestion>`}}", 
                      inline=True)
                    
                    embed4.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    embed4.timestamp = datetime.datetime.utcnow()
                    
                    await m.edit(embed=embed4)

                #This deletes the embed
                # IF reacted with the garbage bin    
                elif str(reaction.emoji) == '<:trash:734043301187158082>':
                    await m.remove_reaction('<:trash:734043301187158082>', member)
                    garb = discord.Embed(
                      color=0x570505)
                    garb.add_field(name="Removing this embed...", value="Your decision but aight 🤷🏽\n\n<:trash:734043301187158082>Removing the embed in 5 seconds...<:trash:734043301187158082>")
                    
                    await m.edit(embed=garb, delete_after=5)

                elif str(reaction.emoji) == '⚠️':
                    await m.remove_reaction('⚠️', member)
                    
                    cog = self.get_cog_by_class('Management')
                    commands = cog.get_commands()
                    command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
                      description="\n\n".join(command_desc), 
                      color=0x623E00)
                      
                    e.timestamp = datetime.datetime.utcnow()
                    
                    e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    await m.edit(embed=e)

                elif str(reaction.emoji) == '🔗':
                    await m.remove_reaction('🔗', member)
                    
                    cog = self.get_cog_by_class('Misc')
                    
                    commands = cog.get_commands()
                    
                    command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n__*Your Available Commands*__", 
                      description="\n\n".join(command_desc), 
                      color=0xB6B6B6)
                    
                    e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    e.timestamp = datetime.datetime.utcnow()
                    
                    await m.edit(embed=e)

                else:
                    if str(reaction.emoji) == '📖':
                        await m.remove_reaction('📖', member)
                        
                        general = self.get_cog_by_class('General')
                        
                        fun = self.get_cog_by_class('Fun')
                        
                        giveaway = self.get_cog_by_class('Giveaway')
                        
                        misc = self.get_cog_by_class('Misc')
                        
                        management = self.get_cog_by_class('Management')
                        
                        e = discord.Embed(
                            title=f'All Commands (Default prefix is `{ctx.prefix}`)',
                            description="__**{{Category Index}}**__", 
                            color=0x232323)
                      
                        e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                        
                        e.add_field(name="📖 Main Menu", value="`Shows this Menu`", inline=True)
                        
                        e.add_field(
                          name=f"{general.qualified_name}", 
                          value=f"{general.description}", 
                          inline=True)
                          
                        e.add_field(
                          name=f"<:fun:734648757441921124> {fun.qualified_name}", 
                          value=f"{fun.description}", 
                          inline=True)
                          
                        e.add_field(
                          name=f"{giveaway.qualified_name}", 
                          value=f"{giveaway.description}", 
                          inline=True)
                        
                        e.add_field(
                          name="📚 Application/Suggestion Category", 
                          value="`List of Application/Suggestion Commands`", 
                          inline=True)
                        
                        e.add_field(name=f"{management.qualified_name}", 
                        value=f"{management.description}", 
                        inline=True)
                      
                        e.add_field(name=f"{misc.qualified_name}", 
                        value=f"{misc.description}", 
                        inline=True)
                        
                        e.add_field(
                          name="<:trash:734043301187158082> Cancellation", 
                          value="`Deletes this Embed/Help Message`", 
                          inline=True)
                          
                        e.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                        
                        await m.edit(embed=e)

    @commands.command()
    async def pages(self, ctx):
        contents = ["This is page 1!", "This is page 2!", "This is page 3!", "This is page 4!"]
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

    @commands.command()
    async def testhelp(self, ctx, *cog):
        """
        Gets all the Commands of Mine
        """
        
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
        
def setup(bot):
    bot.add_cog(Helpdude(bot))
