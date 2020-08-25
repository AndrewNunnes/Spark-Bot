#•----------Modules----------•#

import discord

from discord.ext import commands, tasks

import pathlib

import logging

import platform

import json

from pathlib import Path

import datetime

import os

import asyncio

import aiosqlite

import cogs._json

#•----------Other File Variables----------•#

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n•—•—•—•—•—•—•—•—•—•")

#•--------------Functions--------------•#

#Function for getting the prefix data from a json file
def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
      return commands.when_mentioned_or('!')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

#Function used to load extensions
def file_name(file):
    if file.endswith(".py") and not file.startswith("_"):
      bot.load_extension(f"cogs.{file[:-3]}")
      
#•----------Define Bot Instance----------•#

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.remove_command('help')

#•--------------Change Status---------------•#

#Background task to change bot status
@tasks.loop(seconds=30)
async def change_status():
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Flight take another L"))
    
    await asyncio.sleep(1 * 900)
    
    await bot.change_presence(activity=discord.Game(name="Bots Can Play Basketball Too"))
    
    await asyncio.sleep(1 * 900)
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Jacquees"))
    
    await asyncio.sleep(1 * 900)
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} Lousy Servers"))
    
    await asyncio.sleep(1 * 900)
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Summer Walker"))
    
    await asyncio.sleep(1 * 900)
    
    await bot.change_presence(activity=discord.Game(name="!help"))
    
    await asyncio.sleep(1 * 900)
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} Users"))

    await asyncio.sleep(1 * 900)
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Family Guy"))
    
@change_status.before_loop
async def before_ready():
    await bot.wait_until_ready()
    
#Start the loop
change_status.start()

#•----------When the bot is Ready----------•#
    
#When the bot is ready and running
@bot.event
async def on_ready():

    #Only for me, for quicker code testing
    channel = bot.get_channel(737948764483878975)
    await channel.send("Now online")

    print("Bot is working")
    #Change the bot's status
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Flight take another L"))

#•----------Connect to Database----------•#

#Function to make our life easier
#Used to connect to database
#And create all tables
async def connect_db():
    
    bot.db = await aiosqlite.connect('main.db')
    
    await bot.db.executescript("""
    
    CREATE TABLE IF NOT EXISTS guilds (
    id INTEGER PRIMARY KEY
    );
    
    CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY, 
    guild_id INTEGER, 
    FOREIGN KEY (guild_id) REFERENCES guilds (id)
    );

    CREATE TABLE IF NOT EXISTS warns (
    user_id INTEGER, 
    mod_id INTEGER, 
    reason TEXT, 
    warn_id INTEGER PRIMARY KEY, 
    guild_id INTEGER, 
    FOREIGN KEY (guild_id) REFERENCES guilds (id), 
    FOREIGN KEY (user_id, mod_id) REFERENCES members (member_id, member_id)
    );

    CREATE TABLE IF NOT EXISTS welcome (
    guild_id INTEGER PRIMARY KEY, 
    msg TEXT, 
    channel_id INTEGER, 
    FOREIGN KEY (guild_id) REFERENCES guilds (id)
    ); 
    
    CREATE TABLE IF NOT EXISTS goodbye (
    guild_id INTEGER PRIMARY KEY, 
    msg TEXT, 
    channel_id INTEGER, 
    FOREIGN KEY (guild_id) REFERENCES guilds (id)
    );
    """)
    
    await bot.db.commit()
    #await bot.db.close()

#Make the database
asyncio.get_event_loop().run_until_complete(connect_db())
#client.loop.create_task(connect_db(bot))

#•--------------Prefix--------------•#

#Function for getting the prefix
#From the database
#def get_prefix(client, message):

  #conn = await aiosqlite.connect('main.db')

  #data = conn.fetchone("SELECT prefix FROM prefix_list WHERE GuildID = ?", message.guild.id)
  #return when_mentioned_or(data)(client, message)

bot.cwd = cwd 

@bot.event
async def on_message(message):
  
    #prefix = data[str(message.guild.id)]
  
    #Makes sure the bot doesn't respond to itself
    if message.author == bot.user:
      return
    #Checks for a different bot in the server
    if message.author.bot:
      return
    #When the bot is mentioned, it'll respond with this embed
    if bot.user.mentioned_in(message):
      data = cogs._json.read_json('prefixes')
      if str(message.guild.id) in data:
          prefix = data[str(message.guild.id)]
          if message.content.startswith(prefix):
            return
      else:
        if not str(message.guild.id) in data:
            prefix = '!'
          
        prefixembed = discord.Embed(
          description=f"What's up {message.author.mention}. My prefix is `{prefix}`\nFeel free to change it with `{prefix}prefix <newprefix>`", 
          color=discord.Color.darker_grey())
      
      
        prefixembed.timestamp = datetime.datetime.utcnow()
    
        await message.channel.send(embed=prefixembed)
  
    await bot.process_commands(message)
    
#•---------------------------------•#
    
if __name__ == '__main__':
    #If there's any files inside the cogs
    #That depends on the database being loaded
    #Load the database first
    for file in os.listdir(cwd+"/cogs/datab/"):
        file_name(f'datab.{file}')
        
    for file in os.listdir(cwd+"/cogs/"):
        file_name(file)
        
    for file in os.listdir(cwd+"/cogs/events/"):
        file_name(f'events.{file}')
        
    for file in os.listdir(cwd+"/cogs/other/"):
        file_name(f'other.{file}')

        #Ignore all these old versions
                #if file.endswith(".py") and not file.startswith("_"):
                    #client.load_extension(f"cogs.{file[:-3]}")
    
#for ext in [file.stem for file in pathlib.Path('cogs').glob('**/*.py')]:
    #client.load_extension(f"cogs.{ext}")
    
#for ext in[".".join(p.parts)[:-len(".py")] for p in pathlib.Path('cogs').glob('**/*.py')]:
  #client.load_extension(ext)

bot.run('bruh')
