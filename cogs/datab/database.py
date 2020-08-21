import discord 
from discord.ext import commands

import aiosqlite
import os

#class Database(commands.Cog):
    #def __init__(self, bot):
        #self.bot = bot

#Creating the database, and connecting
async def create_db(client):
    await client.wait_until_ready()

    conn = await aiosqlite.connect('main.db')

    cursor = await conn.cursor()

    #Create tables
    await cursor.executescript("""

    CREATE TABLE IF NOT EXISTS warns (
    user_id	INTEGER,
    reason TEXT,
    guild_id INTEGER,
    PRIMARY KEY(user_id, guild_id)
    ); 
    
    CREATE TABLE IF NOT EXISTS mutes (
    user_id	INTEGER, 
    role_ids TEXT, 
    EndTime	TEXT,
    PRIMARY KEY(user_id)
    );

    CREATE TABLE IF NOT EXISTS prefix_list (
    guild_id INTEGER, 
    prefix TEXT DEFAULT '!', 
    PRIMARY KEY(guild_id)
    );

    CREATE TABLE IF NOT EXISTS welcome (
    guild_id INTEGER, 
    msg TEXT, 
    channel_id INTEGER, 
    PRIMARY KEY(guild_id, channel_id)
    );

    CREATE TABLE IF NOT EXISTS goodbye (
    guild_id INTEGER, 
    msg TEXT, 
    channel_id INTEGER, 
    PRIMARY KEY(guild_id, channel_id)
    );
    
    """)

    await cursor.close()

    await conn.commit()

    await conn.close()
