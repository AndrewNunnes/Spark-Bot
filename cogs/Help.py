import discord
from discord.ext import commands
import asyncio
import logging
import datetime

logging.basicConfig(level = logging.INFO)

class Help_Command(commands.Cog):
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
          inline=True)
        
        e.add_field(
          name=f"{gene.qualified_name}", 
          value=f"{gene.description}", 
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
          
        e.add_field(
          name=f"{management.qualified_name}", 
          value=f"{management.description}", 
          inline=True)
          
        e.add_field(
          name=f"{misc.qualified_name}", 
          value=f"{misc.description}", 
          inline=True)
          
        e.add_field(name="<:trash:734043301187158082> Cancellation", value="`Deletes this Embed/Help Message`", inline=True)
        
        e.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        
        e.set_footer(text="{{Please Remember This Bot Is Not 100% Finished Yet}}")
        
        m = await ctx.send(embed=e)
        
        #Adding the reactions
        reactions = ['📖', '📯', '<:fun:734648757441921124>', '🎉', '📚', '⚙️', '🔗', '<:trash:734043301187158082>']
        for react in reactions:
          await m.add_reaction(react)
          print("Adds reactions")
          
        #Check to make sure no other users can click on the reactions
        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📖', '📯', '<:fun:734648757441921124>', '🎉', '⚙️','📚', '🔗', '<:trash:734043301187158082>']
            print("Check works")
            
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
                    command = cog.get_commands()
                    command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*_\n_*() - Optional\n<> - Required\n\n__*Your Available Commands*_", 
                      description="\n\n".join(command_desc), 
                      color=0x575409)
                    
                    e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    await m.edit(embed=e)
                    print("Below here")
                  
                elif str(reaction.emoji) == '📯':
                    print("Detects")
                    await m.remove_reaction('📯', member)
                    print("Removes reaction")
                    
                    cog = self.get_cog_by_class('General')
                    commands = cog.get_commands()
                    command_desc = [f"• **{c.name}** **:** `{ctx.prefix}{c.usage}`\n• {c.brief}" for c in cog.walk_commands()]
                    print("Cog descs work")
                    
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
                    commands = cog.get_commands()
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
                    
                elif str(reaction.emoji) == '<:trash:734043301187158082>':
                    await m.remove_reaction('<:trash:734043301187158082>', member)
                    garb = discord.Embed(
                      color=0x570505)
                    garb.add_field(name="Removing this embed...", value="Your decision but aight 🤷🏽\n\n<:trash:734043301187158082>Removing the embed in 5 seconds...<:trash:734043301187158082>")
                    
                    await m.edit(embed=garb, delete_after=5)

                elif str(reaction.emoji) == '⚙️':
                    await m.remove_reaction('⚙️', member)
                    
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


def setup(bot):
    bot.add_cog(Help_Command(bot))
