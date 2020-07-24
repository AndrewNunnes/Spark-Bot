import discord
from discord.ext import commands
import random
import asyncio
import datetime

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
            await ctx.send("That channel doesn't exist")
        else:
            await ctx.send(f"Great, the giveaway will start in {channel.mention}\nBut how many winners will there be? (Choose between `1-25`)")
            msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
            s = random.sample(range(1000000), k=25)
            bro = int(msg.content)
            await ctx.send(f"Ok there will be {bro} winners\nHow much time should this giveaway last for?")
            msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
            waitTime = msg.content
            seconds = 0
            giveawaytime = waitTime.split(' ', maxsplit=1)
            unit = giveawaytime[1]
            value = float(giveawaytime[0])
            if unit in ('d', 'D', ' d', ' D', ' days', ' Days', ' day', 'Day', 'Days', 'days', 'day', 'Day'):
                seconds += int(value * 86400)
            elif unit in ('h', 'H', ' h', ' H', ' hour', ' Hour', ' hours', ' Hours', 'hour', 'hours', 'Hour', 'Hours'):
                seconds += int(value * 3600)
            elif unit in (' minute', ' minutes', ' Minute', ' Minutes', 'minute', 'Minute', 'minutes', 'Minutes', 'm', 'M', ' m', ' M'):
                seconds += int(value * 60)
            elif unit in ('s', 'S', ' s', ' S', 'seconds', 'second', 'Second', 'Seconds', ' seconds', ' second', ' Second', ' Seconds'):
                seconds += int(value)
            else:
                raise ValueError("Invalid Token: %s" % giveawaytime)
            await ctx.send(f"Aight, the giveaway will last {waitTime}\nNow what are you giving away?")
            msg = await self.bot.wait_for('message', timeout=25.0, check=is_me)
            three = msg.content
            await ctx.send(f"Aight cool, the giveaway is now starting in :\n{channel.mention}")
            
            await asyncio.sleep(1.75)
            
            giveawayembed = discord.Embed(title="🎉 __**GIVEAWAY**__ 🎉", description=f"__*Prize: {three}*__\n\n__*Lasts: {waitTime}*__\n\n_*Hosted by: {ctx.author.mention}*_", colour=discord.Color.dark_orange())
            giveawayembed.set_footer(text=f"{bro} Winners | Ends ")
            giveawayembed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
            
            giveawaymsg = await channel.send(embed=giveawayembed)
            await giveawaymsg.add_reaction('🎉')
            
            await asyncio.sleep(seconds)
            giveawaymsg = await channel.fetch_message(giveawaymsg.id)
            for reaction in giveawaymsg.reactions:
                if reaction.emoji == '🎉':
                    users = await reaction.users().flatten()
                    list_of_string = []
                    winners = random.sample(users, k=bro)
                    for each in winners:
                        astring = str(each)
                        list_of_string.append(astring)
                        bruh = "\n• ".join(map(str, winners))
                        embed = discord.Embed(title="🎉 __**GIVEAWAY ENDED**__ 🎉", description=f"__*Winner(s):*__\n• {bruh}", color=discord.Color.dark_red())
                        embed.set_footer(text=f"{bro} Winners | Ended ")
                        embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
                        await giveawaymsg.edit(embed=embed)
                await channel.send(f"Congratulations {','.join([x.mention for x in winners])} you won the **{three}**")
                await giveawaymsg.clear_reaction('🎉')
                    
    @commands.command(aliases=["reroll"])
    @commands.has_any_role('Moderator', 'Executive Admin', 'Owner', 'Not Andrew')
    async def end(self, ctx, message: discord.Message):
        giveawaymsg = await ctx.fetch_message(message.id)
        users = await giveawaymsg.reactions.users().flatten()
        winner = random.choice(users)
        new_users = []
        for x in users:
            if x != self.bot.user:
                new_users.append(x)
                users = new_users
        await ctx.send(f'__**{winner.mention} has won the Giveaway!**__')

def setup(bot):
    bot.add_cog(Giveaway(bot))
