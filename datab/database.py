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
    reason	TEXT,
    guild_id	INTEGER,
    PRIMARY KEY(user_id, guild_id)
    ); 
    
    CREATE TABLE IF NOT EXISTS mutes (
    UserID	INTEGER, 
    RoleIDS	TEXT, 
    EndTime	TEXT,
    PRIMARY KEY(UserID)
    );

    CREATE TABLE IF NOT EXISTS prefix_list (
    GuildID INTEGER, 
    prefix TEXT DEFAULT '!', 
    PRIMARY KEY(GuildID)
    );

    CREATE TABLE IF NOT EXISTS welcome (
    guild_id TEXT, 
    msg TEXT, 
    channel_id TEXT, 
    );

    CREATE TABLE IF NOT EXISTS goodbye (
    guild_id TEXT, 
    msg TEXT, 
    channel_id TEXT, 
    );
    
    """)

    await cursor.close()

    await conn.commit()

    await conn.close()

#def setup(bot):
    #bot.add_cog(Database(bot))

#self.bot.loop.create_task(create_db(self.bot))
