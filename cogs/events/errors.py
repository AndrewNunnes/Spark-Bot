import discord
from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #All global errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            
            await ctx.send('~~Command doesn\'t exist bro~~')
            await ctx.message.add_reaction('⛔')
        
        #Checks for Bot Missing Perms
        elif isinstance(error, commands.BotMissingPermissions):
          
          embed = discord.Embed(
            description="Seems like I'm missing some permissions", 
            color=discord.Color.dark_red())
            
          await ctx.send(embed=embed)
        
        #Checks if the Invoker is the Owner of the Bot
        elif isinstance(error, commands.NotOwner):
          
          embed = discord.Embed(description="You're not the Owner of this bot dummy", color=discord.Color.dark_red)
          
          await ctx.send(embed=embed)
        
        elif isinstance(error, commands.NoPrivateMessage):
            
            await ctx.send('~~You can\'t use commands outside of the server~~')
        
        elif isinstance(error, commands.CommandOnCooldown):
            
            guild = ctx.guild
            if not guild:
                await ctx.reinvoke()
            else:
                var1 = error.retry_after
                var2 = int(var1)
                
                await ctx.send(f'You can\'t use this command for another {var2} seconds', delete_after=5)
        
        elif isinstance(error, commands.MissingPermissions):
            
            poo = discord.Embed(description="You don't have the permissions to do that, idiot", color=discord.Color.dark_red())
            
            await ctx.send(embed=poo, delete_after=5)
        
        elif isinstance(error, commands.MissingRequiredArgument):
            
            await ctx.send("Seems like you're forgetting to put something bruh", delete_after=5)
        else:
            raise(error)

def setup(bot):
    bot.add_cog(Errors(bot))
