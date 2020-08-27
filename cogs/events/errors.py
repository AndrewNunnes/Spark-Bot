
#•----------Modules----------•#
import discord

from discord.ext import commands

from discord import Embed

import string

#•----------Functions-----------•#

async def on_bot_forbidden(self, ctx, bot, args2):
    """Handles Missing Bot Permissions Errors"""

    # Convert list into string of the missing permissions
    missing_perms = string.capwords(", ".join(args2.missing_perms).replace("_", " "))

    embed = Embed(description=f"❌ Looks like I'm missing **{missing_perms}** Permission(s) to perform this command ❌",
                colour=0x420000)

    if bot.guild_permissions.send_messages:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")


async def on_command_forbidden(self, ctx, bot):
    """Handles Forbidden Error"""

    embed = Embed(description="**❌ I Don't Have Permissions To Execute This Command ❌**",
                colour=0x420000)

    if bot.guild_permissions.send_messages:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")


async def on_command_bad_argument(self, ctx, bot):
    """Handles Bad Argument Errors (Argument can't be read properly)"""

    embed = Embed(description="**❌ Whoever you tried to mention doesn't exist in this server ❌**",
                colour=0x420000)

    if bot.guild_permissions.send_messages:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")


async def on_command_not_found(self, ctx, bot):
    """Handles the command not found error"""

    embed = Embed(description=f"That command doesn't exist bro ❌ Please use **{ctx.prefix}help** to see all the commands",
                colour=0x420000)

    if bot.guild_permissions.send_messages:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")


async def on_command_cooldown(self, ctx, bot, error):
    """Handles Cooldown Errors"""

    embed = Embed(description=f"That command's on cooldown. Try again in **{error.retry_after:,.2f}** seconds",
                colour=0x420000)

    if bot.guild_permissions.send_messages:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")


async def on_command_permission(self, ctx, bot, args2):
    """Handles User Missing Permissions Errors"""

    # Convert list into string of the missing permissions
    missing_perms = string.capwords(", ".join(args2.missing_perms).replace("_", " "))

    embed = Embed(description=f"❌ Seems like you need **{missing_perms}** Permission(s) use this command ❌",
                colour=0x420000)

    if bot.guild_permissions.send_messages:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")


async def on_command_missing_argument(self, ctx, bot):
    """Handles the missing argument error"""

    embed = Embed(description="Required Argument(s) Missing"
                            f"\nUse **{ctx.prefix}help** to find out how to use `{ctx.command}`",
                colour=0x420000)

    if bot.guild_permissions.send_messages:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")


async def on_not_owner(self, ctx, bot):
    """Handles the error when the user is not the owner and tries to invoke owner only command"""

    embed = Embed(description="**❌ You can't use that command since you're not the Owner of the Bot ❌**",
                colour=0x420000)

    if bot.guild_permissions.send_messages:
        await ctx.send(embed=embed)
    else:
        print("Error: Error Handling Message Could Not Be Sent")

#•-----------Class-----------•#

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, args2):
        """Event to detect and handle errors"""

        # Get Spark ++
        bot = ctx.guild.get_member(self.bot.user.id)

        # if the user did not specify an user
        if isinstance(args2, commands.MissingRequiredArgument):
            await on_command_missing_argument(self, ctx, bot)
        # if the user has spammed a command and invoked a cooldown
        elif isinstance(args2, commands.CommandOnCooldown):
            await on_command_cooldown(self, ctx, bot, args2)
        # if the user tries to access a command that isn't available
        elif isinstance(args2, commands.CommandNotFound):
            await on_command_not_found(self, ctx, bot)
        # if the user provides an argument that isn't recognised
        elif isinstance(args2, commands.BadArgument):
            await on_command_bad_argument(self, ctx, bot)
        # if the user does not the correct permissions to call a command
        elif isinstance(args2, commands.MissingPermissions):
            await on_command_permission(self, ctx, bot, args2)
        # if the bot is missing permissions needed
        elif isinstance(args2, commands.BotMissingPermissions):
            await on_bot_forbidden(self, ctx, bot, args2)
        # if the bot is forbidden from performing the command
        elif isinstance(args2, discord.Forbidden):
            await on_command_forbidden(self, ctx, bot)
        # if the user tries to invoke a command that is only for the owner
        elif isinstance(args2, commands.NotOwner):
            await on_not_owner(self, ctx, bot)
        else:
            raise(args2)

def setup(bot):
    bot.add_cog(Errors(bot))
