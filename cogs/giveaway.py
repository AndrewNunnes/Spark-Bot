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
        await ctx.send("Aight lets start setting up the giveaway\nWhat channel will it be in?")
        msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
        try:
            channel_converter = discord.ext.commands.TextChannelConverter()
            channel = await channel_converter.convert(ctx, msg.content)
        except commands.BadArgument:
            await ctx.send("That channel doesn't exist", delete_after=5)
        else:
            await ctx.send(f"Great, the giveaway will start in {channel.mention}\nBut how many winners will there be? (Choose between `1-25`)")
            msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
            s = random.sample(range(1000000), k=25)
            bro = int(msg.content)
            await ctx.send(f"Ok there will be {bro} winners\nHow many seconds should it last? *Check this link to convert seconds to minutes/hours:* https://bit.ly/37BgQ0L")
            msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
            second = msg.content
            await ctx.send(f"Aight, the giveaway will last {second} seconds\nNow what are you giving away?")
            msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
            three = msg.content
            await ctx.send(f"Aight cool, the giveaway is now starting in {channel.mention}")
            
            await asyncio.sleep(1.75)

            giveawayembed = discord.Embed(title="🎉 __**GIVEAWAY**__ 🎉", description=f"__*Prize: {three}*__\n__*Lasts: {second} seconds*__\n\n_*Hosted by: {ctx.author.mention}*_", colour=discord.Color.dark_orange())
            giveawayembed.set_footer(text="Suggestions or problems? DM Andrew Nunnes#1148!")
            
            giveawaymsg = await channel.send(embed=giveawayembed)
            await giveawaymsg.add_reaction('🎉')
            
            await asyncio.sleep(int(second))
            giveawaymsg = await channel.fetch_message(giveawaymsg.id)
            for reaction in giveawaymsg.reactions:
                if reaction.emoji == '🎉':
                    users = await reaction.users().flatten()
                    list_of_string = []
                    winners = random.sample(users, k=bro)
                    for each in winners:
                        astring = str(each)
                        list_of_string.append(astring)
                        bruh = "\n•".join(map(str, winners))
                        embed = discord.Embed(title="🎉 __**GIVEAWAY ENDED**__ 🎉", description=f"__*Winner(s):*__\n• {bruh}", color=discord.Color.dark_red())
                        embed.set_footer(text="Make sure to claim your prize!")
                        await giveawaymsg.edit(embed=embed)
                        await channel.send(f"Congratulations {','.join([x.mention for x in winners])} you won the **{three}**")
                        await giveawaymsg.clear_reaction('🎉')
                    
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
