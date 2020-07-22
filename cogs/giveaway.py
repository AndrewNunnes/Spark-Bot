import discord
from discord.ext import commands
import random
import asyncio

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def giveaway(self, ctx):
        def is_me(m):
            return m.author == ctx.author
        def checkreact(reaction, user):
            return 
        await ctx.send("I see you want to make a giveaway,\nWhat will the name be?")
        msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
        first = msg.content
        await ctx.send("Ok, so how many seconds should it last? *Check this link to convert seconds to minutes/hours:* https://bit.ly/37BgQ0L")
        msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
        second = msg.content
        await ctx.send("Now what are you giving away?")
        msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
        three = msg.content
        await ctx.send("Giveaway has been created!")

        giveawayembed = discord.Embed(title="A giveaway has appeared!", colour=discord.Color.dark_orange())

        giveawayembed.set_footer(text="Suggestions or problems? DM Andrew Nunnes#1148!")

        giveawayembed.add_field(name=f"{three}", value=f"Giveaway lasts {second} seconds. Hosted by {ctx.author.mention}")
        await asyncio.sleep(2)
        giveawaymsg = await ctx.send(embed=giveawayembed)
        await giveawaymsg.add_reaction('🎉')
        await asyncio.sleep(int(second))
        giveawaymsg = await ctx.channel.fetch_message(giveawaymsg.id)
        users = await giveawaymsg.reactions[0].users().flatten()
        winner = random.choice(users)
        for reaction in giveawaymsg.reactions:
            if reaction.emoji == '🎉':
                    await ctx.send(f"{winner.mention} has won {three}! Congrats!")
                    
    @commands.command(aliases=["endgiveaway"])
    @commands.has_any_role('Moderator', 'Executive Admin', 'Owner', 'Not Andrew')
    async def end(self, ctx, message: discord.Message):
        giveawaymsg = await ctx.fetch_message(message.id)
        users = await giveawaymsg.reactions[0].users().flatten()
        winner = random.choice(users)
        new_users = []
        for x in users:
            if x != self.bot.user:
                new_users.append(x)
                users = new_users
        await ctx.send(f'__**{winner.mention} has won the Giveaway!**__')

def setup(bot):
    bot.add_cog(Giveaway(bot))
