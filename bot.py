import discord
from discord.ext import commands
import pathlib
import logging
import platform
import json
from pathlib import Path
import datetime
import os

import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n•—•—•—•—•—•—•—•—•—•")

#Function for getting the prefix data from a json file
def get_prefix(client, message):
  data = cogs._json.read_json('prefixes')
  if not str(message.guild.id) in data:
    return commands.when_mentioned_or('!')(client, message)
  return commands.when_mentioned_or(data[str(message.guild.id)])(client, message)

#Function used to load extensions
def file_name(file):
    if file.endswith(".py") and not file.startswith("_"):        client.load_extension(f"cogs.{file[:-3]}")

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
client.remove_command('help')

client.cwd = cwd 

@client.event
async def on_message(message):
  
  #prefix = data[str(message.guild.id)]
  
  #Makes sure the bot doesn't respond to itself
  if message.author == client.user:
    return
  #Checks for a different bot in the server
  if message.author.bot:
    return
  #When the bot is mentioned, it'll respond with this embed
  if client.user.mentioned_in(message):
    data = cogs._json.read_json('prefixes')
    if str(message.guild.id) in data:
        prefix = data[str(message.guild.id)]
        if message.content.startswith(prefix):
          return
    else:
        prefix = '!'
        
        prefixembed = discord.Embed(
          description=f"What's up {message.author.mention}. My prefix is `{prefix}`\nFeel free to change it with `{prefix}prefix <newprefix>`", 
          color=discord.Color.darker_grey())
        
        
        prefixembed.timestamp = datetime.datetime.utcnow()
      
        await message.channel.send(embed=prefixembed)
    
  await client.process_commands(message)
  
@client.event
async def on_ready():
    print("Bot is working")
    return await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Flight take another L"))
    
if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs/"):
        file_name(file)
    for file in os.listdir(cwd+"/cogs/events/"):
        file_name(f'events.{file}')
    for file in os.listdir(cwd+"/cogs/other/"):
        file_name('other.{file}')
                #if file.endswith(".py") and not file.startswith("_"):
                    #client.load_extension(f"cogs.{file[:-3]}")
    
#for ext in [file.stem for file in pathlib.Path('cogs').glob('**/*.py')]:
    #client.load_extension(f"cogs.{ext}")
    
#for ext in[".".join(p.parts)[:-len(".py")] for p in pathlib.Path('cogs').glob('**/*.py')]:
  #client.load_extension(ext)
    
client.run("bruh")
