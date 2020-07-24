import discord
from discord.ext import commands
import random
from random import randint
import platform
import logging
import asyncio
import datetime
import typing
import sqlite3
import aiosqlite
import os
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = '!', case_insensitive=True)
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is working')
    return await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Flight take another L'))

extension = ['cogs.help_command', 'cogs.General Commands', 'cogs.Fun Commands', 'cogs.mc', 'cogs.Suggestions', 'cogs.Application', 'cogs.Moderation', 'cogs.Administrator Commands', 'cogs.giveaway', 'cogs.other.global', 'cogs.events.reactions', 'cogs.events.welcome', 'cogs.events.errors']

if __name__ == '__main__':
    for ext in extension:
        client.load_extension(ext)

client.run('bruh')
