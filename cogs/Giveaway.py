import discord
from discord.ext import commands
import random
import asyncio
import datetime
import re

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

def convert(argument):
#"""
#This function will convert X amount of d|h|m|s depending on what they choose into those seconds using the time_dict and time_regex
    
#Params:
  #- self :
  #- argument {argument for the function} : The letter we're choosing
#Returns:
  #- time : Returns the amount of time depending on the letter we choose
#"""
  args = argument.lower()
  matches = re.findall(time_regex, args)
  time = 0
  for key, value in matches:
    try:
      time += time_dict[value] * float(key)
    except KeyError:
      raise commands.BadArgument(f"{value} is an invalid time key! `h|m|s|d` are valid time keys")
    except ValueError:
      raise commands.BadArgument(f"{key} isn't even a number dummy")
  return time
    
class Giveaway(commands.Cog):
  
  """🎉 `{Commands for Hosting Giveaways}`"""
  
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(
    brief="{Quicksetup for the Giveaway} [NOT DONE]", 
    usage="quickgiveaway <#channel> <winners> <time> <prize>")
  @commands.guild_only()
  @commands.has_permissions(kick_members=True)
  async def quickgiveaway(self, ctx):
    """
    Refined version of the giveaway below {NOT DONE}
    """
    
    def is_me(m):
      return m.author == ctx.author
    questions = ["Aight let's start setting up this giveaway. What channel will it be in?", "Great the giveaway will be in {channel}\nHow many winners will there be? (Choose between `1-25`)", "Ok there will be {winners} winner(s)\n\nHow much time should this giveaway last? Say X amount of `d|h|m|s`", "Aight the giveaway will last {time}\nNow what are you giving away?"
        ]
    answers = {}
    for question in questions:
      answer = await GetGiveawayMessage(self.bot, ctx, contentOne=question, timeout=100.0)
      
      if not answer:
          #User failed to answer the question
        await ctx.send(f"You failed to answer: `{question}`, please be quicker next time")
        return
        
      else:
        print("This works")
        #Giveaway will be made
        await ctx.send(f"Great the giveaway will start in {channel.mention} and the prize is {prize}")
        print("Channel works")
          
          #We have a valid answer to the question, now let's store the answers
      answers[questions.index(question)] = answer
          
      description = " "
      for key, value in answers.items():
        print("This also works")
        addition = f"{key+1} {questions[key]}\n{value}\n\n"
            
      await asyncio.sleep(1.75)
      print("Giveaway starting works")
          
      giveawayembed = discord.Embed(
        title="🎉 __**GIVEAWAY**__ 🎉",
        description=key,
        color=discord.Color.dark_orange())
          
      reaction = await ctx.send(embed=embed)
      print("Giveaway sends")
      await reaction.add_reaction('🎉')
              
  @commands.command(
    brief="{Interactively Sets Up the Giveaway}", 
    usage="startgiveaway")
  @commands.guild_only()
  @commands.has_permissions(kick_members=True)
  async def startgiveaway(self, ctx):
    """
    Sloppy Version but still works perfectly
    """
    def is_me(m):
      return m.author == ctx.author
    await ctx.send("Aight lets start setting up the giveaway\nWhat channel will it be in?") #Starts setting up the giveaway
    while True:
      try:
        msg = await self.bot.wait_for('message', timeout=60.0, check=is_me)
        channel_converter = discord.ext.commands.TextChannelConverter() #Converts the channel mentioned
        channel = await channel_converter.convert(ctx, msg.content)
      except commands.BadArgument:
        await ctx.send("Bruh that channel doesn't even exist. Try again")
            #Raises exception made in the TimeConverter
      else:
          await ctx.send(f"Great, the giveaway will start in {channel.mention}\nBut how many winners will there be? (Choose between `1-25`)")
          msg = await self.bot.wait_for('message', timeout=60.0, check=is_me)
          break
    while True:
        try:
          s = random.sample(range(1000000), k=25)
          bro = int(msg.content) #Converts the number of winners into a number/int for later on
        except ValueError:
          await ctx.send("You really thought that was a number? Try again") #Errors if the amount of winners isn't a number
          msg = await self.bot.wait_for('message', timeout=60.0, check=is_me)
        else:
          await ctx.send(f"Ok there will be {bro} winners\nHow much time should this giveaway last for?\nPlease say one of these options: `#d|#h|#m|#s`")
          msg = await self.bot.wait_for('message', timeout=60.0, check=is_me)
          break
    while True:
        try:
          time = int(convert(msg.content))
          #convert is the word from the TimeConverter Function at the top of the file, to convert the x amount of d|h|m|s
        except ValueError:
          await ctx.send("That isn't an option. Please choose x amount of `d|h|m|s`")
          msg = await self.bot.wait_for('message', timeout=60.0, check=is_me)
        else:
          break
    await ctx.send(f"Aight, the giveaway will last {time}s\nNow what are you giving away?")
    msg = await self.bot.wait_for('message', timeout=60.0, check=is_me)
    prize = msg.content #The item we're giving away
    print("This works")
    await ctx.send(f"Aight cool, the giveaway is now starting in :\n{channel.mention}")
          
    await asyncio.sleep(1.75)
          
    giveawayembed = discord.Embed(title="🎉 __**GIVEAWAY**__ 🎉", description=f"__*REACT With 🎉 to participate!*__", colour=discord.Color.darker_grey())
    
    giveawayembed.add_field(name="_*Prize:*_", value=f"🏆 {prize}")
    giveawayembed.add_field(name=f"_*Lasts:*_", value=f"__**{time}s**__")
    
    giveawayembed.set_author(name=f"Hosted by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
    
    giveawayembed.set_footer(text=f"{bro} Winners | Ends ")
    
    giveawayembed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
                
    sendgiveaway = await channel.send(embed=giveawayembed)
    await sendgiveaway.add_reaction('🎉')

    for number in range(int(time), 0, -5): 
        #Edits the original giveaway embed to create a countdown for the timer
      timecounter = discord.Embed(title="🎉 __**GIVEAWAY**__ 🎉", description=f"__*REACT With 🎉 to participate!*__\n\n", colour=discord.Color.darker_grey())
      
      timecounter.set_footer(text=f"{bro} Winner(s) | Ends ")
      
      timecounter.set_author(name=f"Hosted by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
      
      timecounter.add_field(name="_*Prize:*_", value=f"🏆 {prize}")
      timecounter.add_field(name="_*Time Left:*_", value=f"_*{number}s*_")
      
      timecounter.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=number)     
      
      await sendgiveaway.edit(embed=timecounter)
      await asyncio.sleep(5)
      
    sendgiveaway = await channel.fetch_message(sendgiveaway.id)
    for reaction in sendgiveaway.reactions:
      if reaction.emoji == '🎉':
        #Checks for the users that reacted to 🎉
          users = await reaction.users().flatten()
          list_of_string = []
          winners = random.sample(users, k=bro)
          for each in winners:
            astring = str(each)
            list_of_string.append(astring)
            bruh = "\n• ".join(map(str, winners))
            embed = discord.Embed(title="🎉 __**GIVEAWAY ENDED**__ 🎉", description=f"__*Winner(s):*__\n• {bruh}", color=discord.Color.darker_grey())
            
            embed.add_field(name="Prize:", value=f"🏆 {prize}")
            
            embed.set_author(name=f"Hosted by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
            
            embed.set_footer(text=f"{bro} Winners | Ended ")
            
            embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=number)
            
            await sendgiveaway.edit(embed=embed)
    await channel.send(f"🎉 Congratulations {','.join([x.mention for x in winners])} you won: **{prize}** 🎉")
    await sendgiveaway.clear_reaction('🎉')
                    
  @commands.command(
    brief="{Rerolls a New Winner for the Giveaway}", 
    usage="reroll <message_id>")
  @commands.guild_only()
  @commands.has_permissions(kick_members=True)
  async def reroll(self, ctx, message: discord.Message):
      """
      Ends the giveaway manually {NOT 100% FUNCTIONAL YET}
      """
      giveawaymsg = await ctx.fetch_message(message.id)
      users = await giveawaymsg.reactions.users().flatten()
        
      new_users = []
      for x in users:
          if x != self.bot.user:
              new_users.append(x)
              users = new_users
      await ctx.send(f'__**{winner.mention} is the new winner!**__')

async def GetGiveawayMessage(bot, ctx, contentOne="Test Message", timeout=90.0):
    """
    This function waits for a message to be returned from a user
    
    Params:
    - bot {commands.Bot Object} :
    - ctx {context object} : Used for sending messages
    - Optional Params:
        - timeout {int} : Timeout for the wait_for
    Returns:
    - msg.content {string} : If a message is detected the content will be returned
    - False {boolean} : If the timeout occurs it will return False
    """
    await ctx.send(f"{contentOne}")
    try:
        msg = await bot.wait_for('message', timeout=timeout, check=None)
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False

def setup(bot):
    bot.add_cog(Giveaway(bot))
