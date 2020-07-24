import discord
from discord.ext import commands
import datetime
import asyncio

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Welcoming new Members
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            embed = discord.Embed(colour=discord.Colour.dark_green(), description=f"What's up {member}, and welcome to the server! You are now member {len(list(member.guild.members))}")
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"Welcome {member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(id=721630160448782367)

            message = await channel.send(embed=embed)
            await message.add_reaction("<:callme:729502466592210966>")
        except Exception as error:
            raise (error)

    #Saying goodbye to leaving members
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(colour=discord.Colour.dark_red(), description=f"{member} just left the server. Thanks for visiting! Member Count: {len(list(member.guild.members))}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"Goodbye {member.name}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        channel = self.bot.get_channel(id=721630160448782367)

        message = await channel.send(embed=embed)
        await message.add_reaction("<:waving:729500876288557109>")

def setup(bot):
    bot.add_cog(Welcome(bot))
