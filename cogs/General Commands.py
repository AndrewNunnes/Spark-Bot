import discord
from typing import Optional
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import platform
import datetime
import random
import asyncio

class General(commands.Cog):

    """{_*General Commands You Can Use*_}"""

    def __init__(self, bot):
        self.bot = bot
            
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1 , 30, type=BucketType.channel)
    async def binfo(self, ctx):
        """
        `Shows info about the bot`
        """
        
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        embed = discord.Embed(title='My Info', color=discord.Color.dark_red())
        embed.add_field(name='My Owner:', value="Andrew Nunnes#1148", inline=True)
        embed.add_field(name='Python Version:', value=f"I'm running version {pythonVersion} of Python", inline=True)
        embed.add_field(name='Discord Version:', value=f"I'm running Discord Version {dpyVersion}", inline=True)
        embed.add_field(name='Server Count:', value=f"I'm in {serverCount} server(s)", inline=True)
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 30, type=BucketType.channel)
    async def sinfo(self, ctx):
        """
        `Shows the stats/info of the server`
        """

        memberCount = len(set(self.bot.get_all_members()))
        poo = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        pee = len(list(filter(lambda m: m.bot, ctx.guild.members)))

        statuses = [len(list(filter(lambda m: str(m.status) == "online" , ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle" , ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd" , ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline" , ctx.guild.members)))]

        embed = discord.Embed(title=f'My Stats/Server Info', color=0x000000)
        embed.set_footer(text=f'Created · {ctx.guild.created_at.strftime("%d/%m/%Y")}')
        embed.set_author(name=f"Command requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name='Name:', value=ctx.guild.name, inline=True)
        embed.add_field(name='Region:', value=ctx.guild.region, inline=True)
        embed.add_field(name='Owner:', value=ctx.guild.owner, inline=True)
        embed.add_field(name='Member Count:', value=f'<:online:728377717090680864>{statuses[0]}, <:idle:728377738599071755>{statuses[1]}, <:dnd:728377763458973706>{statuses[2]}, <:offline:728377784207933550>{statuses[3]}\nTotal: {memberCount}', inline=True)
        embed.add_field(name='Banned Members:', value=f'{len(await ctx.guild.bans())}', inline=True)
        embed.add_field(name='Humans:', value=f'{poo} Humans', inline=True)
        embed.add_field(name='Bots:', value=f'{pee} Bots', inline=True)
        embed.add_field(name='Channels:', value=f'<:textch:728377808518381679>{len(ctx.guild.text_channels)}\n<:voicech:728377834187259976>{len(ctx.guild.voice_channels)}', inline=True)
        embed.add_field(name='Invites:', value=f'{len(await ctx.guild.invites())}', inline=True)
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(3, 15, type=BucketType.user)
    async def ping(self, ctx):
        """
        `Runs a connection test to discord`
        """
        embed = discord.Embed(title='Pong?', color=discord.Color.dark_blue())
        await ctx.send(embed=embed, delete_after=0.3)
            
        await asyncio.sleep(0.5)
            
        embed = discord.Embed(title='My Connection:', description=f'__**My ping is {round(self.bot.latency * 1000)}ms**__', color=discord.Color.dark_blue())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(3, 20, type=BucketType.user)
    async def uinfo(self, ctx, member: discord.Member = None):
        """
        `Shows info about you`
        """

        member = ctx.author if not member else member
        roles = [role for role in member.roles]

        embed = discord.Embed(title=f"{{{member.name}'s General Info}}", description=f"**>Discord Tag: **{member}\n**>Nick: **{member.nick}\n**>User ID: **{member.id}\n**>Created: **{member.created_at.strftime('%a %#d %B %Y, %I:%M %p')}\n**>Joined: **{member.joined_at.strftime('%a %#d %B %Y, %I:M %p')}\n**>Roles {{{len(roles)}}}': **{' '.join([role.mention for role in roles])}\n**>Top Role: **{member.top_role.mention}", colour=0x000000)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(3, 20, type=BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        """`Get an enlarged version of somebody's avatar`"""
        member = ctx.author if not member else member
        userinfo = member
        embed = discord.Embed(title=f"{userinfo.name}'s Avatar", color=0x000000, timestamp = datetime.datetime.utcnow())
        embed.set_author(name=f"Command requested by: {ctx.message.author}")
        embed.set_image(url=userinfo.avatar_url_as(format='png'))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
