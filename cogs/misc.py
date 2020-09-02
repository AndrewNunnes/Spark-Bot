#•----------Modules----------•#

import discord

import asyncio

import random

from datetime import datetime

from discord.ext.commands import BucketType, command, bot_has_permissions, guild_only, Cog, cooldown, has_permissions, MissingRequiredArgument

from typing import Optional

#•----------Class----------•#

def to_emoji(c):
    base = 0x1f1e6
    return chr(base+c)

class Misc(Cog, name="Misc Category"):

    """`{Miscallaneous Commands}`"""

    def __init__(self, bot):
        self.bot = bot
        
#•----------Commands----------•#
    
    @command(
        brief="{Leave any Feedback for the Owner of the Bot}", 
        usage="feedback <message_here>")
    @guild_only()
    @cooldown(1, 86400.0, BucketType.user)
    async def feedback(self, ctx, *, fb):
        pass
        
    #Booster Command  
    @command(
        brief="{List of Boosters for the Server}", 
        usage="boosters", 
        aliases=['sboosters', 'boosts', 'boosterlist'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    @bot_has_permissions(use_external_emojis=True)
    async def boosters(self, ctx):

        booster_list = []
        
        boost = ctx.guild.premium_subscribers

        #If there's over 25 boosters
        if len(boost) > 25:
            #Subtract 25
            length = boost - 25
              
            #Showing the 25 members and if there's more
            #We show the leftover
            booster_list = f"{' , '.join(map(str, (member.mention for member in list(reversed(boost))[:25])))} and **{length}** more..."
            
        else:
            #Show all members if less than 25
            booster_list = f"{' , '.join(map(str, (member.mention for member in list(reversed(boost[1:])))))}"

        #Make a variable to make stuff easier
        boosters = "No Members" if booster_list == [] else booster_list

        #Make embed
        e = discord.Embed(
            title=f"<:booster:741407205575622696> __**List of Boosters for {{{ctx.guild.name}}}**__", 
            color=0x420000, 
            timestamp=datetime.utcnow())
            
        #Make fields
        fields = [
                ("*Members who Boosted*", 
                    
                f"{boosters}", True)]
            
        #Add fields
        for n, v, i in fields:
            e.add_field(
                name=n, 
                value=v, 
                inline=i)

        e.set_footer(
            text=f"{len(boost)} Total")
      
        await ctx.send(embed=e)

    @command(
        brief="{Leave a Suggestion}", 
        usage="suggest <suggestion>", 
        aliases=['sugg'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def suggest(self, ctx, *, sug):
      
        #If the suggestion is too long
        if len(sug) > 750:
            e = discord.Embed(
                description="<:redmark:738415723172462723> __*Suggestion can't be longer than 750 Characters*__", 
                color=0x420000)
            await ctx.send(embed=e)
            return
      
        #Look for a keyword 'sugg' in a channel
        channel = discord.utils.find(lambda g: 'sugg' in g.name, ctx.guild.text_channels)
           
        #If there isn't a suggestion channel
        if not channel:
            await ctx.send("I can't seem to find a Suggestion channel")
            return
       
        #Make embed
        e = discord.Embed(
            title="__*New Suggestion!*__", 
            description=f"{sug}\n** **", 
            color=0x420000)
          
        e.set_thumbnail(
            url=ctx.author.avatar_url)
      
        e.set_footer(
            text=f"Provided by {ctx.author}")
          
        e.timestamp = datetime.utcnow()
      
        #Delete author's message
        await ctx.message.delete()
      
        #Make the embed fields
        fields = [
                  ("__*React to Leave your Opinion!*__", 
                  "<:greenmark:738415677827973152> - __*Good*__" +
                  "\n<:redmark:738415723172462723> - __*Bad*__" +
                  "\n<:maybemark:738418156808175616> - __*Maybe/Ok*__", True)]
      
        #Add fields
        for n, v, i in fields:
            e.add_field(
                name=n, 
                value=v, 
                inline=i)
      
        #Send the embed
        m = await channel.send(embed=e)
      
        #List the reactions   
        reactions = ["<:greenmark:738415677827973152>", "<:redmark:738415723172462723>", "<:maybemark:738418156808175616>"]
      
        #Add reactions
        for react in reactions:
            await m.add_reaction(react)

    @command(
      brief="{Bot Interactively Starts a Poll}", 
      usage="poll")
    @guild_only()
    @cooldown(1, 3, BucketType.user)
    async def poll(self, ctx, *, question):

        #A list of messages to delete when we're all done
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
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send('Missing the question.', delete_after=4)

    @command(
      brief="{Start a poll quickly}", 
      usage="quickpoll <at_least_2_questions>")
    @cooldown(1, 3, BucketType.user)
    @guild_only()
    async def quickpoll(self, ctx, *questions_and_choices: str):

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
            
    @command(
        brief="{Apply for Moderator}", 
        usage="applymod")
    @cooldown(1, 3, BucketType.user)
    @guild_only()
    async def applymod(self, ctx, member: discord.Member = None):

        member = member or ctx.author

        def checkreact(reaction, user):
            return user.id == member.id and str(reaction.emoji) in ["✅", "❌"]

        applicationQuestions = [
            "What's your Minecraft IGN + Discord Username?",
            "How old are you? (If you feel uncomfortable saying this, just confirm if you're at least a teenager)",
            "What Time Zone do you live in? (So I know when you're online, and gives me a reason if you're not too active)",
            "Why do you want to be Moderator? Isn't it fun to play without any responsibilites?",
            "What will you do for the Discord Server?",
            "Anything else you want to say?",
        ]
        
        await ctx.send("__*Application will be sent to you soon...*__")
        
        applicationAnswers = {}
        for question in applicationQuestions:
            answer = await GetMessage(self.bot, member=member, contentOne=question, timeout=500)
            
            if not answer:
              #They failed to provide an answer
              await member.send(f"You failed to answer: `{question}`\nBe quicker next time")
              return

            # We have a valid answer to a question, lets store it
            applicationAnswers[applicationQuestions.index(question)] = answer
            print(answer)

        # We finished asking questions, lets check they want to submit this before sending it off
        confirmation = await member.send("Are you sure you want to submit this application?")
        await confirmation.add_reaction("✅")
        await confirmation.add_reaction("❌")

        reaction, user = await self.bot.wait_for(
            "reaction_add", timeout=60.0, check=checkreact
        )
        if str(reaction.emoji) == "✅":
            async with member.typing():
                await member.send(
                    "Thank you for applying! Your application will be sent to the Owner soon"
                )

                # We need to sus out whether or not to split the application into separate
                # embeds or not due to embed ratelimits
                descriptionChunks = {}

                description = ""
                for key, value in applicationAnswers.items():
                    addition = f"{key+1}) {applicationQuestions[key]}\n{value}\n\n"

                    if (len(description) + len(addition)) > 1850 and len(addition) <= 1850:
                        # This is gonna be to big for 1 embed together, but its gucci on its own
                        # so lets split it and make 2 embeds

                        # Lets make the bigger of the two into a descriptionChunks and the other description
                        if len(description) > len(addition):
                            # the current description is bigger
                            descriptionChunks[description] = False
                            description = addition
                        else:
                            # the addition is bigger
                            descriptionChunks[addition] = False
                        continue

                    elif len(addition) > 1850:
                        # This line alone is to big for one embed description
                        if len(addition) < 2850:
                            # It can still technically fit into 1 embed
                            partOne = addition[:1850]
                            partTwo = addition[1850:]
                            descriptionChunks[partOne] = {'multipleEmbeds': False, 'fieldValue': partTwo}
                        else:
                            # Technically, it has to be less then 4k words or
                            # else we would not have been able to send ours
                            # and vice versa so make 2 embeds
                            partOne = addition[:1850]
                            partTwo = addition[1850:]
                            descriptionChunks[partOne] = False
                            descriptionChunks[partTwo] = False
                        continue

                    else:
                        # We should be safe to simply add this to our current
                        # description and carry on as we are
                        description += addition
                        continue

                else:
                    if description != "":
                        descriptionChunks[description] = False

                for key, value in descriptionChunks.items():
                    applicationEmbed = discord.Embed(
                        title="Application Answers __**{MODERATOR}**__",
                        description=key,
                        color=discord.Color.dark_purple(),
                        timestamp=datetime.utcnow()
                    )
                    applicationEmbed.set_author(
                        name=f"Application taken by: {member.display_name}", icon_url=f"{member.avatar_url}"
                    )
                    applicationEmbed.set_footer(text=f"{member.display_name}")

                    if value != False:
                        # We need to add a field for the rest of the data
                        applicationEmbed.add_field(name='\uFEFF', value=value['fieldValue'])
                    
                    channelnames = ['application']
                    #Checks for a channel with an Application keyword to send this to
                    channel = discord.utils.find(
                      lambda channel:any(
                        map(lambda c: c in channel.name, channelnames)), ctx.guild.text_channels)
                    
                    #Checks if a application channel doesn't exist    
                    if not channel:
                      otherchann = ['gener', 'chat', 'welc']
                      newchann = discord.utils.find(
                        lambda newchann:any(
                          map(lambda n: n in newchann.name, otherchann)), ctx.guild.text_channels)
                      await newchann.send("I can't seem to find the Application channel containing a keyword {`application`} to send everybody's applications")

                    await channel.send(embed=applicationEmbed)

        elif str(reaction.emoji) == "❌":
            await member.send("Application won't be sent")


async def GetMessage(
    bot, member, contentOne="Default Message", contentTwo="\uFEFF", timeout=500
):
    """
    This function sends an embed containing the params and then waits for a message to return

    Params:
     - bot (commands.Bot object) :
     - member (member object) : Used for sending members the embed
     
     - Optional Params:
        - contentOne (string) : Embed title
        - contentTwo (string) : Embed description
        - timeout (int) : Timeout for wait_for

    Returns:
     - msg.content (string) : If a message is detected, the content will be returned
    or
     - False (bool) : If a timeout occurs
    """
    embed = discord.Embed(title=f"{contentOne}", description=f"{contentTwo}", color=discord.Color.darker_grey())
    async with member.typing():
        await asyncio.sleep(2)
        await member.send(embed=embed)
    
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeout,
            check=lambda message: message.author == member and message.guild == None)
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False

#•----------Setup/Add Cog----------•#
def setup(bot):
    bot.add_cog(Misc(bot))
