import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime

#import datetime
#import textwrap
#import traceback

#import lightbulb
#import hikari
#from hikari.models.intents import Intent

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)

class Misc(commands.Cog):

    """🔗 `{Miscallaneous Commands}`"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
      brief="{Create a Pernament Invite for a Channel}", 
      usage="createinvite <#channel>")
    @commands.has_permissions(create_instant_invite=True)
    @commands.guild_only()
    async def createinvite(self, ctx, channel: discord.TextChannel):
        """
        `Creates an Invite for a Specified Channel`
        """
        invite = await channel.create_invite()
        await ctx.send(invite)
        
    #@invite.error
    #async def invite_error(self, ctx, error):
      #  if isinstance(error, commands.NotOwner):
          #  embed = discord.Embed(description#="You can't use this command!", color=discord.Color.dark_red())
          #  embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
          #  await ctx.channel.send(embed=e
    @commands.command(
      brief="{Bot will announce your message}", 
      usage="announce (channel) <message_here>")
    #@commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def announce(self, ctx, channel: discord.TextChannel=None, *, arg):
      
        if channel is None:
            await ctx.send(arg)
        
        if channel is not None:
            await channel.send(arg)

   # @announce.error
  #  async def announce_error(self, ctx, error):
   #     if isinstance(error, commands.MissingRequiredArgument):
         #   embed = discord.Embed(description=f'Please include the message\n```!announce >message<```', color=discord.Color.dark_red())
        #    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
          #  await ctx.channel.send(embed=embed, delete_after=5)
      #  elif isinstance(error, commands.NotOwner):
         #   embed = discord.Embed(description=f"You can't use this command!", color=discord.Color.dark_red())
         #   embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
         #   await ctx.channel.send(embed=embed, delete_after=5)
            
    @commands.command(
      brief="{DM a User}", 
      usage="dm <user> <message>")
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def dm(self, ctx, user:discord.User, *, content):
        
        await user.send(content)
        
        await ctx.send(f"Successfully sent {user} a dm")
            
    @commands.command(
      brief="{Bot Interactively Starts a Poll}", 
      usage="poll")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
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
        embed = discord.Embed(title=f"{ctx.author} asks: {question}", description=f"\n{answer}\n", color=discord.Color.dark_gold())
        actual_poll = await ctx.send(embed=embed)
        for emoji, _ in answers:
            await actual_poll.add_reaction(emoji)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('Missing the question.', delete_after=4)

    @commands.command(
      brief="{Start a poll quickly}", 
      usage="quickpoll <at_least_2_questions>")
    @commands.guild_only()
    #@commands.has_permissions(manage_messages=True)
    async def quickpoll(self, ctx, *questions_and_choices: str):
        """Makes a poll quickly.
        The first argument is the question and the rest are the choices.
        """

        if len(questions_and_choices) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.', delete_after=5)
        elif len(questions_and_choices) > 21:
            return await ctx.send('You can only have up to 20 choices.', delete_after=5)

        perms = ctx.channel.permissions_for(ctx.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Need Read Message History and Add Reactions permissions.', delete_after=5)

        question = questions_and_choices[0]
        choices = [(to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])]

        try:
            await ctx.message.delete()
        except:
            pass

        body = "\n".join(f"{key}: {c}" for key, c in choices)
        
        embed = discord.Embed(
            title=f"{ctx.author} asks: {question}", 
            description=f"\n{body}\n")
        
        poll = await ctx.send(embed=embed)
        for emoji, _ in choices:
            await poll.add_reaction(emoji)
            
    @commands.command(
      brief="{Get a List of Guilds the Bot's in}", 
      usage="bguilds", 
      aliases=['botguilds'])
    @commands.guild_only()
    @commands.is_owner()
    async def bguilds(self, ctx):

        #Empty String 
        #To add guild names later
        g_list = ''
        
        #Iterate through servers bot's in
        for g in self.bot.guilds:
            #Add the guild names
            #To the empty string
            g_list += f'• {"".join(g.name)}\n'
        
        #Make embed
        e = discord.Embed(
            title=f"__*Total Guilds {{{len(self.bot.guilds)}}}*__", 
            description=g_list)
        
        e.timestamp = datetime.utcnow()
        
        e.set_footer(
            text=ctx.author, 
            icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=e)
            
    @commands.command(
      brief="{Restart the Bot} [BOT OWNER ONLY]", 
      usage="shutdown", 
      aliases=['logout', 'turnoff'])
    @commands.is_owner()
    @commands.guild_only()
    async def shutdown(self, ctx):
      
        await ctx.message.delete()
        
        await ctx.send("I'm shutting down now 👋🏽", delete_after=5)
        
        await asyncio.sleep(1)
        
        await self.bot.logout()

def setup(bot):
    bot.add_cog(Misc(bot))
