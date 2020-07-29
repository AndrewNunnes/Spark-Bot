import discord
from discord.ext import commands
import asyncio
import logging

logging.basicConfig(level = logging.INFO)

class Help_Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Creates A New Help Command


    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        
        member = ctx.author if not member else member
        embed = discord.Embed(title=f'All Commands (Default prefix is "{ctx.prefix}")')

        embed.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n♣️ __**General Commands**__ {Commands showing things such as serverinfo, userinfo, etc.}\n\n<:fun:734648757441921124> __**Fun Commands**__ {Variety of Different Fun Commands}\n\n<:grass:734647227523268668> __**Minecraft Commands**__ {Minecraft Related Fun Commands}\n\n🎉 __**Giveaway**__ {Commands for Giveaways}\n\n📑 __**Application Commands**__ {Commands to apply for something}\n\n📫 __**Suggestion Commands**__ {Commands to leave a Suggestion}\n\n🔐 __**Moderation Commands**__ {Commands to Moderate the server (Mods and Admins Only)}\n\n🔗 __**Misc Commands**__ {Misc Commands Only Mods and Admins can Use}", inline=True)
        embed.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        m = await ctx.send(embed=embed)
        await m.edit(embed=embed)
        await m.add_reaction('📖')
        await m.add_reaction('♣️')
        await m.add_reaction('<:fun:734648757441921124>')
        await m.add_reaction('<:grass:734647227523268668>')
        await m.add_reaction('🎉')
        await m.add_reaction('📑')
        await m.add_reaction('📫')
        await m.add_reaction('🔐')
        await m.add_reaction('🔗')
        await m.add_reaction('<:trash:734043301187158082>')
        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📖', '♣️', '<:fun:734648757441921124>', '<:grass:734647227523268668>', '🎉', '📑', '📫', '🔐', '🔗', '<:trash:734043301187158082>']
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=45.0, check=checkreact)

            except asyncio.TimeoutError:
                bruh = discord.Embed(color=discord.Color.dark_red())
                bruh.add_field(name="__**What were you doing?**__", value="You took too long to react with an emoji bruh 🤦🏽")
                bruh.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                await m.edit(embed=bruh)
            else:
                if str(reaction.emoji) == '🎉':
                    await m.remove_reaction('🎉', member)
                    bruh = discord.Embed(title=f'Giveaway Commands (Default prefix is "{ctx.prefix}")', color=0x919234)
                    bruh.add_field(name="__**Commands:**__", value="_*giveaway*_ - {Creates the giveaway interactively}\n\n_*end*_(gend, endgiveaway) - {Ends a giveaway using the messageid}", inline=True)
                    await m.edit(embed=bruh)
                if str(reaction.emoji) == '♣️':
                    await m.remove_reaction('♣️', member)
                    embed1 = discord.Embed(title=f'General Commands (Default prefix is "{ctx.prefix}")', color=discord.Color.darker_grey())

                    embed1.add_field(name="__**Commands:**__", value="_*binfo*_ - {Shows info about the Bot}\n\n_*sinfo*_ - {Shows info about the server}\n\n_*uinfo*_ - {Shows info about a user}\n\n_*avatar*_ - {Shows the avatar of a user}\n\n_*ping*_ - {Runs a connection test to Discord}", inline=True)
                    await m.edit(embed=embed1)
            
                elif str(reaction.emoji) == '<:fun:734648757441921124>':
                    await m.remove_reaction('<:fun:734648757441921124>', member)
                    embed2 = discord.Embed(title=f'Fun Commands (Default prefix is "{ctx.prefix}")', color=discord.Color.dark_blue())

                    embed2.add_field(name="__**Commands:**__", value="_*8ball*_ - {Ask a question and get an answer}\n\n_*letschat(chat)*_ - {Have a convo with the Bot}\n\n_*fact*_ - {Get a random fact}\n\n_*spotify*_ - {See who's listening to Spotify}\n\n_*insta*_ - {Get info on an Insta Account}\n\n_*meme*_ - {Get a random meme}\n\n_*embed*_ - {Make your message a fancy embed}\n\n_*bottles*_(!bottles 7 water) - {x bottles of x on the wall}\n\n_*add*_(4+4) - {Add two numbers together}\n\n_*hug*_ - {Hug someone}\n\n_*punch*_ - {Punch somebody}\n\n_*slap*_ - {Slap someone}\n\n_*iq*_ - {Says your IQ}\n\n_*gay*_ - {Shows how gay you are}\n\n_*penis*_ - {Says your penis size}\n\n_*thot*_ - {Says how much of a thot you are}\n\n_*hack_* - {Hack somebody}\n\n_*coinflip*_ - {Flip a coin}\n\n_*playball(playb)*_ - {Will you win a basketball game?}", inline=True)
                    await m.edit(embed=embed2)

                elif str(reaction.emoji) == '<:grass:734647227523268668>':
                    await m.remove_reaction('<:grass:734647227523268668>', member)
                    embed3 = discord.Embed(title=f'Minecraft Commands (Default prefix is "{ctx.prefix}")', color=0xa0722a)

                    embed3.add_field(name="__**Commands:**__ ", value="_*mcping(!mcping play.hypixel.net)*_ - {Shows stats of a Minecraft server}\n\n_*skin*_ - {Get the skin of another Player}\n\n_*uuid*_ - {Get the UUID of another Player}\n\n_*getplayer*_ - {Get a Player username with their UUID]\n\n_*mcsales*_ - {Shows the sales of Minecraft}\n\n_*buildidea*_ - {Get a random build idea}\n\n_*colorcodes*_ - {Get the colorcodes of Minecraft Text}", inline=True)
                    await m.edit(embed=embed3)

            
                elif str(reaction.emoji) == '📑':
                    await m.remove_reaction('📑', member)
                    embed4 = discord.Embed(title=f'Application Commands (Default prefix is "{ctx.prefix}")', color=0x223ba3)

                    embed4.add_field(name="__**Commands:**__", value="_*applymod*_ - {Apply for Moderator}", inline=True)
                    await m.edit(embed=embed4)

                elif str(reaction.emoji) == '📫':
                    await m.remove_reaction('📫', member)
                    embed5 = discord.Embed(title=f'Suggestion Commands (Default prefix is "{ctx.prefix}")', color=0x223ba3)

                    embed5.add_field(name="__**Commands:**__", value="_*suggest*_ - {Leave a suggestion}", inline=True)
                    await m.edit(embed=embed5)
                    
                elif str(reaction.emoji) == '<:trash:734043301187158082>':
                    await m.remove_reaction('<:trash:734043301187158082>', member)
                    garb = discord.Embed(color=discord.Color.dark_red())
                    garb.add_field(name="Removing this embed...", value="Your decision but aight 🤷🏽\n\n<:trash:734043301187158082>Removing the embed in 5 seconds...<:trash:734043301187158082>")
                    await m.edit(embed=garb, delete_after=5)

                elif str(reaction.emoji) == '🔐':
                    await m.remove_reaction('🔐', member)
                    embed6 = discord.Embed(title=f'Moderation Commands(Mods and Admins **Only**) (Default prefix is "{ctx.prefix}")', color=0x9a9a23)

                    embed6.add_field(name="__**Commands:**__", value="_*kick*_ - {Kicks a User}\n\n_*ban*_ - {Bans a User}\n\n_*unban*_(!unban User name#1234) - {Unbans a User}\n\n_*mute*_ - {Mutes a user from texting for a specified amount of time}\n\n_*unmute*_ - {Manually Unmutes a User}\n\n_*purge(prune, clean)*_ - {Deletes a specified amount of messages}", inline=True)
                    await m.edit(embed=embed6)

                elif str(reaction.emoji) == '🔗':
                    await m.remove_reaction('🔗', member)
                    embed7 = discord.Embed(title=f'Misc Commands(Mods and Admins **Only**) (Default prefix is "{ctx.prefix}")', color=0x62239a)

                    embed7.add_field(name="__**Commands:**__", value="_*invite(!invite #channelname)*_ - {Creates an invite for a specific channel}\n\n_*announce*_ - {Bot will say whatever the User says}\n\n_*dm*_ - {DM a User a custom message}\n\n_*poll*_ - {Creates a Poll}\n\n_*quickpoll*_ - {Creates a poll quickly}\n\n_*restart(shutdown)*_ - {Restart/Shutdown the Bot (Owner **Only**)}", inline=True)
                    await m.edit(embed=embed7)

                else:
                    if str(reaction.emoji) == '📖':
                        await m.remove_reaction('📖', member)
                        embed0 = discord.Embed(title=f'All Commands (Default prefix is "{ctx.prefix}")')

                        embed0.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n♣️ __**General Commands**__ {Commands showing things such as serverinfo, userinfo, etc.}\n\n<:fun:734648757441921124> __**Fun Commands**__ {Variety of Different Fun Commands}\n\n<:grass:734647227523268668> __**Minecraft Commands**__ {Minecraft Related Fun Commands}\n\n🎉 __**Giveaway**__ {Commands for Giveaways}\n\n📑 __**Application Commands**__ {Commands to apply for something}\n\n📫 __**Suggestion Commands**__ {Commands to leave a Suggestion}\n\n🔐 __**Moderation Commands**__ {Commands to Moderate the server (Mods and Admins Only)}\n\n🔗 __**Misc Commands**__ {Misc Commands Only Mods and Admins can Use}", inline=True)
                        embed0.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                        await m.edit(embed=embed0)


def setup(bot):
    bot.add_cog(Help_Command(bot))
