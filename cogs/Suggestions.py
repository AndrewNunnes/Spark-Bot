import discord
from discord.ext import commands
import datetime
from discord.ext.commands.cooldowns import BucketType

class Suggestions(commands.Cog):

    """{_*Commands for Suggestions*_}"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(5, 30, type=BucketType.user)
    async def suggest(self, ctx, *, sug):
        """
        `Leave a suggestion!`
        """
        await ctx.message.delete()
        try:
            embed = discord.Embed(description=f"__*Suggestion provided by {ctx.author.mention}*__: {sug}\n\nReact down below to leave your opinion! ⬇️\n\n<:greenmark:738415677827973152> {{Yes}}\n<:redmark:738415723172462723> {{No}}\n<:maybemark:738418156808175616> {{Maybe}}", color=discord.Color.dark_purple())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.timestamp = datetime.datetime.utcnow()
            #channelnames = ['suggest', 'suggestions']
            #for channel_const in ctx.guild.text_channels:
              #for chann in channelnames:
                #if chann in channel_const.name:
                  #channel = channel_const
                 # break
                #if not chann:
                 # await ctx.send("I can't seem to find a suggestion channel")
            
            channel = discord.utils.find(lambda g: 'sugg' in g.name, ctx.guild.text_channels)
            
            if not channel:
              await ctx.send("I can't seem to find a Suggestion channel")
                 
            poo = await channel.send(embed=embed)
            await poo.add_reaction("<:greenmark:738415677827973152>")
            await poo.add_reaction("<:redmark:738415723172462723>")
            await poo.add_reaction("<:maybemark:738418156808175616>")
            
        except Exception as error:
            raise(error)

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            embed = discord.Embed(description='⚠️ You\'re supposed to include the suggestion dummy ⚠️\n```!suggest <suggestion>```', color=discord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed, delete_after=5)


def setup(bot):
    bot.add_cog(Suggestions(bot))
