import discord
from discord.ext import commands

class Help_Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Creates A New Help Command


    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, member: discord.Member = None):
        
        member = ctx.author if not member else member
        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            
        while True:
            try: 
                embed = discord.Embed(title=f'All Commands (Default prefix is "!")')

                embed.add_field(name="__**Command Index**__", value="""
                0️⃣ This Page
                1️⃣ General Commands
                2️⃣ Fun Commands
                3️⃣ Minecraft Commands
                4️⃣ Application Commands
                5️⃣ Suggestion Commands
                6️⃣ Moderation Commands
                7️⃣ Misc Commands""", inline=False)
    
                m = await ctx.send(embed=embed)
                await m.add_reaction('0️⃣')
                await m.add_reaction('1️⃣')
                await m.add_reaction('2️⃣')
                await m.add_reaction('3️⃣')
                await m.add_reaction('4️⃣')
                await m.add_reaction('5️⃣')
                await m.add_reaction('6️⃣')
                await m.add_reaction('7️⃣')

            except TimeoutError:
                pass
            else:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=checkreact)
                if str(reaction.emoji) == '1️⃣':
                    embed1 = discord.Embed(title=f'Fun Commands (Default prefix is "!")')

                    embed1.add_field(name="__**Fun**__", value="""
                    whois (Mention User)
                    pfp (Mention User)
                    confess (confession)
                    sticks (Mention User)
                    rick (Mention User)
                    meme""", inline=False)
                    await m.edit(embed=embed1)
            
                elif str(reaction.emoji) == '2️⃣':
                    embed2 = discord.Embed(title=f'Emoji Commands (Default prefix is "!")')

                    embed2.add_field(name="__**Emojis**__", value="""
                    thumbsup
                    thumbsdown
                    clown
                    shrug
                    oof
                    wut""", inline=False)
                    await m.edit(embed=embed2)

                elif str(reaction.emoji) == '3️⃣':
                    embed3 = discord.Embed(title=f'Admin Commands (Default prefix is "!")')

                    embed3.add_field(name="__**Administrator**__ ", value="""
                    kick (Mention User) (Reason)
                    ban (Mention User) (Reason)
                    unban (Username And Four Numbers On The End)
                    move (Mention User) (Voice Channel ID)
                    dm (Mention User) (Message)
                    say (Channel) (Message)
                    purge (Amount)
                    """, inline=False)
                    await m.edit(embed=embed3)

            
                elif str(reaction.emoji) == '4️⃣':
                        embed4 = discord.Embed(title=f'Misc Commands (Default prefix is "!")')

                        embed4.add_field(name="__**Misc**__", value="""
                        queue (Your Username)
                        suggest (Suggestion)
                        invite
                        ping
                        support
                        donate""", inline=False)
                        await m.edit(embed=embed4)


                else:
                    if str(reaction.emoji) == '0️⃣':
                        embed0 = discord.Embed(title=f'All Commands (Default prefix is "!")')

                        embed0.add_field(name="__**Command Index**__", value="""
                    0️⃣ This Page
                    1️⃣ General Commands
                    2️⃣ Fun Commands
                    3️⃣ Minecraft Commands
                    4️⃣ Application Commands
                    5️⃣ Suggestion Commands
                    6️⃣ Moderation Commands
                    7️⃣ Misc Commands""", inline=False)
            
                        await m.edit(embed=embed0)


def setup(bot):
    bot.add_cog(Help_Command(bot))
