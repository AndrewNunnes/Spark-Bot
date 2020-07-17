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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #error = getattr(error, 'original, error')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('~~Command doesn\'t exist bro~~')
            await ctx.message.add_reaction('⛔')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('~~You can\'t use commands outside of the server~~')
        elif isinstance(error, commands.CommandOnCooldown):
            guild = ctx.guild
            if not guild:
                await ctx.reinvoke()
            else:
                var1 = error.retry_after
                var2 = int(var1)
                await ctx.send(f'You can\'t use this command for another {var2} seconds')
        elif isinstance(error, commands.MissingPermissions):
            poo = discord.Embed(description="You don't have the permissions to do that, idiot", color=discord.Color.dark_red())
            await ctx.send(embed=poo)
            raise(error)
            
    @commands.command(pass_context=True)
    @commands.cooldown(1, 120, type=BucketType.member)
    async def help(self,ctx,*cog):
        """_**Gets all Categories and commands of mine**_"""
        try:
            if not cog:
                """_**Category Listing.  What more?**_"""
                halp=discord.Embed(title='__Command Categories and Uncategorized Commands__',
                                   description='Use `!help *category*` to find out more about them!\n{Remember to type the category with a **Capital** Letter}',
                                   color=0x908e8c)
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('__*{}*__ - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                halp.add_field(name='__*Categories*__',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                halp.add_field(name='__*Uncategorized/Testing Commands*__',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('',embed=halp)
                await ctx.channel.send("_*The list of commands has been sent to you 📨*_")
            else:
                """__*Helps me remind you if you type too many categories*__"""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='That is way too many categories!',color=discord.Color.dark_red())
                    await ctx.message.author.send('',embed=halp)
                else:
                    """__*Command listing within a category*__"""
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__, color=0x908e8c)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=True)
                                found = True
                    if not found:
                        """__*Reminds you if that category doesn't exist*__"""
                        halp = discord.Embed(title='Error!',description='Pretty sure "'+cog[0]+'"doesnt exist...',color=discord.Color.dark_red())
                    else:
                        await ctx.message.add_reaction(emoji='✉')
                    await ctx.message.author.send('',embed=halp)
        except:
            await ctx.send("Excuse me, I can't send embeds.")
            
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
        embed.add_field(name='My Owner:', value=ctx.guild.owner, inline=True)
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
        embed.add_field(name='Emojis:', value=f"<:rosa:727397157946261534>, <:diamondpick:728333326905114664>, <:diamond:728346793221554307>, <:cake:728347970172616756>, <:enderpearl:728347994922942616>, <:oh:728348048434135200>, <:thonk:728348256236470333>, <:yas:728348281217745079>, <:fyou:728348086598107247>", inline=True)
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

        embed = discord.Embed(title=f'{member.name}', description=f"This shows the User Info of {member.name}", colour=0x000000)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Discord Tag:', value=member, inline=True)
        embed.add_field(name='Nick:', value=member.nick, inline=True)
        embed.add_field(name='ID:', value=member.id, inline=True)
        embed.add_field(name='Created On:', value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=True)
        embed.add_field(name='Joined at:', value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=True)
        embed.add_field(name=f'Roles ({len(roles)}):', value=" ".join([role.mention for role in roles]))
        embed.add_field(name=f"Top Role:", value=member.top_role.mention)

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