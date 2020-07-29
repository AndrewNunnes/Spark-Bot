import discord
from discord.ext import commands
import datetime
import asyncio

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #Sends a fancy embed to show the prefixes    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
      names = ['gener', 'chat', 'memb', 'welc']
      channel = discord.utils.find(
        lambda channel:any(
          map(lambda w: w in channel.name, names)),
        guild.text_channels) #When the bot joins a server, this will check for a general or welcome channel, to send an embed
      #channel = discord.utils.find(lambda **kwargs: kwargs.value())(one='gener', two='chat', three='welc', four='memb', fi
      embed = discord.Embed(color=discord.Color.darker_grey(),
      description=f"What's up everyone! Type `!help` to see all of my commands and get started!\n\n")
      embed.timestamp = datetime.datetime.utcnow()
      await channel.send(embed=embed)
    
    #Welcoming new Members
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            embed = discord.Embed(colour=discord.Colour.dark_green(), description=f"What's up {member}, and welcome to the server! You are now member {len(list(member.guild.members))}")
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"Welcome {member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            
            #channelnames = ['mem', 'new', 'member', 'user', 'User', 'gateway', 'gate', 'entrance', 'enter']
            #for channel_const in member.guild.text_channels:
              #for chann in channelnames:
               # if chann in channel_const.name:
                 # channel = channel_const
                  #break {Complicated version of the lambda function, but still works}
            namelist = ['memb', 'new', 'user', 'User', 'gate', 'enter', 'entr']
            channel = discord.utils.find(any(map(lambda c: c in c.name, namelist)), member.guild.text_channels) #Checks for a keyword inside a channel name
            
            if not channel:
              newlist = ['gener', 'chat', 'welc']
              newchann = discord.utils.find(any(map(lambda n: n in n.name, newlist)), member.guild.channels)
              await newchann.send("Welcome and Goodbye messages to new users won't be sent without the channel including a keyword `new`, `memb` or `user`") #Tries to find a general chat channel to send this error in case the channel doesn't exist
            message = await channel.send(embed=embed)
            await message.add_reaction("🤙🏽")
        except Exception as error:
            raise (error)

    #Saying goodbye to leaving members
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(colour=discord.Colour.dark_red(), description=f"{member} just left the server. Thanks for visiting! Member Count: {len(list(member.guild.members))}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"Goodbye {member.name}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        channelnames = ['memb', 'new', 'user', 'User', 'gateway', 'gate', 'entrance', 'enter']
       # for channel_const in member.guild.text_channels:
         # for chann in channelnames:
            #if chann in channel_const.name:
              #channe {Ignore this}
        channel = discord.utils.find(any(map(lambda c: c in c.name, channelnames)), member.guild.text_channels)
        
        if not channel:
          newlist = ['gener', 'chat', 'welc']
          newchann = discord.utils.find(any(map(lambda n: n in n.name, newlist)), member.guild.text_channels)
          await newchann.send("Welcome and Goodbye messages to new users won't be sent without the channel including a keyword `new`, `memb` or `user`") #In case the channel doesn't exist to welcome new people, this will find a different general or chat channel to send the error to
        message = await channel.send(embed=embed)
        await message.add_reaction("👋🏽")

def setup(bot):
    bot.add_cog(Welcome(bot))
