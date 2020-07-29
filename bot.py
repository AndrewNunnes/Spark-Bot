import discord
from discord.ext import commands
import pathlib
import logging
import platform

client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), case_insensitive=True)
client.remove_command('help')

@client.event
async def on_ready():
    print("Bot is working")
    return await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Flight take another L"))
    
#for ext in [file.stem for file in pathlib.Path('cogs').glob('**/*.py')]:
    #client.load_extension(f"cogs.{ext}")
    
for ext in[".".join(p.parts)[:-len(".py")] for p in pathlib.Path('cogs').glob('**/*.py')]:
  client.load_extension(ext)
    
client.run("bruh")
