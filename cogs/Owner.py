#•----------Modules----------•#
import discord

from discord.ext.commands import command, Cog, BucketType, is_owner, guild_only

from datetime import datetime

import asyncio

#•----------Class----------•#
class Owner(Cog, name="Owner Category"):
  
    """`{Commands for the One and Only Bot Owner}`"""
  
    def __init__(self, bot):
        self.bot = bot
        
#•----------Commands----------•#
            
    @command(
      brief="{Get a List of Guilds the Bot's in}", 
      usage="bguilds", 
      aliases=['botguilds'])
    @guild_only()
    @is_owner()
    async def bguilds(self, ctx):

        #Empty String 
        #To add guild names later
        g_list = ''
        
        #Iterate through servers bot's in
        for g in self.bot.guilds:
            
            name_owner = f"{g.name} **{{{len(g.members)} Mem}}** - {g.owner}"
            #Add the guild names
            #To the empty string
            g_list += f'• {"".join(name_owner)}\n'

        #Make embed
        e = discord.Embed(
            title=f"__*Total Guilds {{{len(self.bot.guilds)}}}*__", 
            description=g_list)
        
        e.timestamp = datetime.utcnow()
        
        e.set_footer(
            text=ctx.author, 
            icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=e)
            
    @command(
      brief="{Shutdown the Bot}", 
      usage="shutdown", 
      aliases=['logout', 'turnoff'])
    @is_owner()
    @guild_only()
    async def shutdown(self, ctx):
        
        await ctx.send("I'm shutting down now 👋🏽")
        
        await asyncio.sleep(1)
        
        #Makes bot logout
        await self.bot.logout

#•----------Setup/Add this Cog----------•#
def setup(bot):
    bot.add_cog(Owner(bot))
