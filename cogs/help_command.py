import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', invoke_without_command=True)
    async def helpcommand(self, ctx):
        embed = discord.Embed(title="All Categories of Commands", color=discord.Color.dark_grey())
        embed.add_field(name="General Commands", value="`!help General`", inline=False)
        embed.add_field(name="Fun Commands", value="`!help Fun`", inline=False)
        embed.add_field(name="Minecraft Commands", value="`!help Minecraft`", inline=False)
        embed.add_field(name="Application Commands", value="`!help Application`", inline=False)
        embed.add_field(name="Suggestion Commands", value="`!help Suggestions`", inline=False)
        embed.add_field(name="Moderation Commands", value="`!help Moderation`", inline=False)
        embed.add_field(name="Misc Commands", value="`!help Misc`", inline=False)
        await ctx.send(embed=embed)

    @helpcommand.group(name="General")
    async def general_subcommand(self, ctx):
        await ctx.send("general commands")

def setup(bot):
    bot.add_cog(Help(bot))
