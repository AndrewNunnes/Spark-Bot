import discord
from typing import Optional
from discord.utils import get
from discord.ext import commands

def syntax(command):
    cmd_and_aliases = "|".join([str(commands), *command.aliases])
    params = []

    for key, value in command.param.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"```{cmd_and_aliases} {params}```"

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cmd_help(self, ctx, command):
        embed = discord.Embed(title=f"`{command}", description=syntax(command), color=discord.Color.dark_magenta())
        embed.add_field(name="Command Description", value=command.help)
        await ctx.send(embed=embed)


    @commands.command(name='help')
    async def show_help(self, ctx, cmd: Optional[str]):
        """Shows this message"""
        if cmd is None:
            pass

        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)

            else:
                await ctx.send("That command doesn't exist bruh")

def setup(bot):
    bot.add_cog(Help(bot))
