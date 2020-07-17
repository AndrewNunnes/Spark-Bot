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
            embed = discord.Embed(description=f"__*Suggestion provided by {ctx.author.mention}*__: {sug}\n\nReact down below to leave your opinion! ⬇️", color=discord.Color.dark_purple())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            embed.timestamp = datetime.datetime.utcnow()
            channel = ctx.guild.get_channel(726689140862746664)
            poo = await channel.send(embed=embed)
            await poo.add_reaction("☑️")
            await poo.add_reaction("🚫")
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