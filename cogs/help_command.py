import discord
from discord.ext import commands
import asyncio
import logging
import datetime

logging.basicConfig(level = logging.INFO)

class Help_Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Creates A New Help Command


    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        
        member = ctx.author if not member else member
        
        #Gets the Cogs
        general = self.bot.get_cog('♠️ General Category')
        fun = self.bot.get_cog('Fun Category')
        
        embed = discord.Embed(
            title=f'All Commands (Default prefix is `{ctx.prefix}`)',
            description="__**{{Category Index}}**__",
            color=discord.Color.darker_grey())
        
        embed.add_field(name="📖 Main Menu", value="`Shows this Menu`", inline=True)
        embed.add_field(
          name=f"{general.qualified_name}", 
          value=f"{general.description}", inline=True)

        embed.add_field(name=f"<:fun:734648757441921124> {fun.qualified_name}", value=f"{fun.description}", inline=True)

        embed.add_field(name="🎉 Giveaway Category", value="`List of Commands Related to Hosting Giveaways`", inline=True)
        embed.add_field(name="📚 Application/Suggestion Category", value="`List of Application/Suggestion Commands`", inline=True)

        embed.add_field(name="🔐 Management Category", value="`Commands Used to Moderate the Server`", inline=True)

        embed.add_field(name="🔗 Misc Category", value="`Miscallaneous Commands`", inline=True)
        embed.add_field(name="<:trash:734043301187158082> Cancellation", value="`Deletes this Embed/Help Message`", inline=True)
        
        embed.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        
        embed.set_footer(text="{{Please Remember This Bot Is Not 100% Finished Yet}}")
        
        m = await ctx.send(embed=embed)
        reactions = ['📖', '♠️', '<:fun:734648757441921124>', '🎉', '📚', '🔐', '🔗', '<:trash:734043301187158082>']
        for reaction in reactions:
          await m.add_reaction(reaction)

        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📖', '♣️', '<:fun:734648757441921124>', '🎉', '🔐','📚', '🔗', '<:trash:734043301187158082>']
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=45.0, check=checkreact)

            except asyncio.TimeoutError:
                bruh = discord.Embed(color=discord.Color.darker_grey())
                bruh.add_field(name="__**What were you doing?**__", value="You took too long to react with an emoji bruh 🤦🏽")
                bruh.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                await m.edit(embed=bruh)
            else:
                if str(reaction.emoji) == '🎉':
                    await m.remove_reaction('🎉', member)
                    
                    bruh = discord.Embed(
                      title=f'Giveaway Category  (Default prefix is `{ctx.prefix}`)', 
                      description="_*() - Optional\n<> - Required*_", 
                      color=0x919234)
                    
                    bruh.add_field(name="_*giveaway*_", value=f"{{`{ctx.prefix}giveaway`}}", inline=True)
                    bruh.add_field(name="_*end(gend, endgiveaway)*_", 
                    value=f"{{`{ctx.prefix}end <themessageid>`}}", 
                    inline=True)
                    
                    bruh.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    await m.edit(embed=bruh)
                  
                elif str(reaction.emoji) == '♣️':
                    await m.remove_reaction('♣️', member)
                    
                    e = discord.Embed(
                      title=f'General Category (Default prefix is `{ctx.prefix}`)', 
                      description="_*() - Optional\n<> - Required*_", 
                      color=discord.Color.darker_grey())
                      
                    cog = self.bot.get_cog('♠️ General Category')
                    commands = cog.get_commands()
                    command_desc = [f"_*{c.name}*_ - `{c.brief}`" for c in cog.walk_commands()]
                    
                    e.add_field(
                      name="\200", 
                      value="\n".join(command_desc))
                    e.timestamp = datetime.datetime.utcnow()
                    
                    e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=e)
            
                elif str(reaction.emoji) == '<:fun:734648757441921124>':
                    await m.remove_reaction('<:fun:734648757441921124>', member)

                    
                    #Used for getting all commands from the "Fun" Cog  
                    cog = self.bot.get_cog('Fun Category')
                    commands = cog.get_commands()
                    command_desc = [f"_*{c.name}*_ - `{c.brief}`" for c in cog.walk_commands()]
                    
                    e = discord.Embed(
                      title=f"__*{cog.qualified_name}*__", 
                      description="_*() - Optional\n<> - Required*_", 
                      color=discord.Color.dark_blue())
                      
                    e.add_field(
                      name="\200", 
                      value="\n".join(command_desc))
                      
                    e.timestamp = datetime.datetime.utcnow()

                    
                    e.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")

                    await m.edit(embed=e)

            
                elif str(reaction.emoji) == '📚':
                    await m.remove_reaction('📚', member)
                    embed4 = discord.Embed(title=f'Application/Suggestion Category (Default prefix is `{ctx.prefix}`)', color=0x223ba3)

                    embed4.add_field(name="_*applymod {Apply for Mod}*_", value=f"{{`{ctx.prefix}applymod`}}", inline=True)
                    embed4.add_field(name="_*suggest {Leave a Suggestion}*_", value=f"{{`{ctx.prefix}suggest <suggestion>`}}", inline=True)
                    
                    embed4.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=embed4)

                    
                elif str(reaction.emoji) == '<:trash:734043301187158082>':
                    await m.remove_reaction('<:trash:734043301187158082>', member)
                    garb = discord.Embed(color=discord.Color.darker_grey())
                    garb.add_field(name="Removing this embed...", value="Your decision but aight 🤷🏽\n\n<:trash:734043301187158082>Removing the embed in 5 seconds...<:trash:734043301187158082>")
                    
                    await m.edit(embed=garb, delete_after=5)

                elif str(reaction.emoji) == '🔐':
                    await m.remove_reaction('🔐', member)
                    embed = discord.Embed(
                      title=f'Management Category (Mods and above **Only**) (Default prefix is "{ctx.prefix}")', 
                      description="_*() - Optional\n<> - Required*_", 
                      color=0x9a9a23)
                    
                    embed.add_field(name="_*prefix {Change the Prefix of the Guild}*_", value=f"{{`{ctx.prefix}prefix <new_prefix>`}}", inline=True)
                    embed.add_field(name="_*role {Menu for Role Management}*_", value=f"{{`{ctx.prefix}role`}}", inline=True)
                    embed.add_field(name="_*kick {Kicks a Member from the Guild}*_", value=f"{{`{ctx.prefix}kick <themember>`}}", inline=True)
                    embed.add_field(name="_*ban {Bans a User from the Guild}*_", value=f"{{`{ctx.prefix}ban <member>`}}", inline=True)
                    embed.add_field(name="_*unban {Unbans a User from the Guild}*_", value=f"{{`{ctx.prefix}unban <User#1234>`}}", inline=True)

                    embed.add_field(name="_*purge(prune, clean) {Deletes a Specified Number of Messages}*_",value=f"{{`{ctx.prefix}purge/clean/prune <amount>`}}", inline=True)

                    
                    embed.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=embed)

                elif str(reaction.emoji) == '🔗':
                    await m.remove_reaction('🔗', member)
                    embed = discord.Embed(title=f'Misc Commands(Mods and Admins **Only**) (Default prefix is "{ctx.prefix}")', color=0x62239a)
                    
                    embed.add_field(name="_*createinvite {Creates a Pernament Invite Link}*_", value=f"{{`{ctx.prefix}createinvite <#channel_name>`}}", inline=True)
                    embed.add_field(name="_*invite {Invite the Bot to your Guild}*_", value=f"{{`{ctx.prefix}invite`}}", inline=True)
                    embed.add_field(name="_*announce {Bot will repeat your message}*_", value=f"{{`{ctx.prefix}announce <your_message>`}}", inline=True)
                    embed.add_field(name="_*dm {DM a Specified User}*_", value=f"{{`{ctx.prefix}dm <user> <message>`}}", inline=True)
                    embed.add_field(name="_*poll {Creates a Poll Interactively}*_", value=f"{{`{ctx.prefix}poll`}}", inline=True)
                    embed.add_field(name="_*quickpoll {Creates a Poll Quickly}*_", value=f"{{`{ctx.prefix}quickpoll <question> <answers>`}}", inline=True)
                    embed.add_field(name="_*restart(shutdown) {Restarts the Bot(Only Owner of the Bot can do this*_", value=f"{{`{ctx.prefix}restart/shutdown`}}", inline=True)

                    
                    embed.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=embed)

                else:
                    if str(reaction.emoji) == '📖':
                        await m.remove_reaction('📖', member)
                        
                        general = self.bot.get_cog('♠️ General Category')
                        fun = self.bot.get_cog('Fun Category')
                        
                        embed0 = discord.Embed(
                            title=f'All Commands (Default prefix is `{ctx.prefix}`)',
                            description="__**{{Category Index}}**__", 
                            color=discord.Color.darker_grey())
                        

                        embed0.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                        embed0.add_field(name="📖 Main Menu", value="`Shows this Menu`", inline=True)
                        embed0.add_field(
                          name=f"{general.qualified_name}", 
                          value=f"{general.description}")

                        embed0.add_field(
                          name=f"<:fun:734648757441921124> {fun.qualified_name}", 
                          value=f"{fun.description}")
                        embed0.add_field(name="🎉 Giveaway Category", value="`List of Commands Related to Hosting Giveaways`", inline=True)
                        embed0.add_field(name="📚 Application/Suggestion Category", value="`List of Application/Suggestion Commands`", inline=True)
                        embed0.add_field(name="🔐 Moderation Category", value="`Commands Used to Moderate the Server`", inline=True)

                        embed0.add_field(name="🔗 Misc Category", value="`Miscallaneous Commands`", inline=True)
                        embed0.add_field(name="<:trash:734043301187158082> Cancellation", value="`Deletes this Embed/Help Message`", inline=True)
                        embed0.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                        await m.edit(embed=embed0)


def setup(bot):
    bot.add_cog(Help_Command(bot))
