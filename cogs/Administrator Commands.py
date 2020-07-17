import discord
from discord.ext import commands
import asyncio
import random

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)

class Misc(commands.Cog):

    """{_*Only Admins and Moderators can use!*_}"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['inv'])
    @commands.is_owner()
    @commands.guild_only()
    async def invite(self, ctx, channel: discord.TextChannel):
        """
        `Creates an Invite for a Specified Channel`
        """
        invite = await channel.create_invite()
        await ctx.send(invite)
        
    @invite.error
    async def invite_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(description="You can't use this command!", color=discord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed)
        raise(error)

    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def announce(self, ctx, *, arg):
        """
        `Announces a custom message`
        """
        await ctx.send(arg)

    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description=f'Please include the message\n```!announce >message<```', color=discord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed, delete_after=5)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(description=f"You can't use this command!", color=discord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed, delete_after=5)
            
    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def dm(self, ctx, user:discord.User, *, content):
        """
        `DM a user`
        """
        await user.send(content)
        await ctx.send(f"{user} just got sent the dm")

    @dm.error
    async def dm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg = ['You\'re supposed to include the user, idiot', 'You forgot the user bruh', 'Are you sending it to a ghost?']
            embed = discord.Embed(description=f'⚠️ {random.choice(msg)} ⚠️\n ```!dm <@user>```', color=discord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(description=f"You can't use this command!", color=discord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed)
            
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role('Moderator', 'Executive Admin')
    async def poll(self, ctx, *, question):
        """Interactively creates a poll with the following question.
        To vote, use reactions!
        """

        # a list of messages to delete when we're all done
        messages = [ctx.message]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100

        for i in range(20):
            messages.append(await ctx.send(f'Say poll option or {ctx.prefix}cancel to publish poll.'))

            try:
                entry = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                break

            messages.append(entry)

            if entry.clean_content.startswith(f'{ctx.prefix}cancel'):
                break

            answers.append((to_emoji(i), entry.clean_content))

        try:
            await ctx.channel.delete_messages(messages)
        except:
            pass # oh well

        answer = '\n'.join(f'{keycap}: {content}' for keycap, content in answers)
        actual_poll = await ctx.send(f'{ctx.author} asks: {question}\n\n{answer}')
        for emoji, _ in answers:
            await actual_poll.add_reaction(emoji)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('Missing the question.', delete_after=4)

    @commands.command()
    @commands.guild_only()
    @commands.has_any_role('Moderator', 'Executive Admin')
    async def quickpoll(self, ctx, *questions_and_choices: str):
        """Makes a poll quickly.
        The first argument is the question and the rest are the choices.
        """

        if len(questions_and_choices) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len(questions_and_choices) > 21:
            return await ctx.send('You can only have up to 20 choices.')

        perms = ctx.channel.permissions_for(ctx.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Need Read Message History and Add Reactions permissions.')

        question = questions_and_choices[0]
        choices = [(to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])]

        try:
            await ctx.message.delete()
        except:
            pass

        body = "\n".join(f"{key}: {c}" for key, c in choices)
        poll = await ctx.send(f'{ctx.author} asks: {question}\n\n{body}')
        for emoji, _ in choices:
            await poll.add_reaction(emoji)
            
    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def restart(self, ctx):
        """
        `Shuts down the Bot`
        """
        await ctx.message.delete()
        await ctx.send("I'm restarting now 👋🏽", delete_after=5)
        
        await asyncio.sleep(1)
        
        await self.bot.logout()
        
    @restart.error
    async def restart_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(description="You can't use this command!", color=discord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed)
        raise(error)

def setup(bot):
    bot.add_cog(Misc(bot))