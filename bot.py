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

DIR = os.path.dirname(__file__)
SQL = None

async def main():
    global SQL
    async with aiosqlite.connect(os.path.join(DIR, "BankAccounts.db")) as db:
        SQL = await db.cursor()
        START_BALANCE = 100
        C_NAME = "Basketballs"
asyncio.run(main())

@client.event
async def on_ready():
    print('Bot is working')
    return await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Flight take another L'))



@client.event
async def on_member_join(member):
    try:
        embed = discord.Embed(colour=discord.Colour.dark_green(), description=f"What's up {member}, and welcome to the server! You are now member {len(list(member.guild.members))} !")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"Welcome {member.name}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        channel = client.get_channel(id=721630160448782367)

        message = await channel.send(embed=embed)
        await message.add_reaction("<:callme:729502466592210966>")
        
        await asyncio.sleep(1)
        
        embed = discord.Embed(title="Welcome to the Server!", description="My prefix is `!` Make sure to **VERIFY** yourself in the (rules-verify) channel to access the rest of the Discord and make sure to read the rules.\nEnjoy your stay 😉", color=discord.Color.dark_blue())
        await member.send(embed=embed)
    except Exception as error:
        raise (error)

@client.event
async def on_member_remove(member):
    embed = discord.Embed(colour=discord.Colour.dark_red(), description=f"{member} just left the server. Thanks for visiting! Member Count: {len(list(member.guild.members))}")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"Goodbye {member.name}", icon_url=f"{member.avatar_url}")
    embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()

    channel = client.get_channel(id=721630160448782367)

    message = await channel.send(embed=embed)
    await message.add_reaction("<:waving:729500876288557109>")

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 733354307298132078:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == "🎉":
            role = discord.utils.get(guild.roles, name="Giveaway")
        elif payload.emoji.name == "🔔":
            role = discord.utils.get(guild.roles, name="Announcements")
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("done")

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 733354307298132078:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == "🎉":
            role = discord.utils.get(guild.roles, name="Giveaway")
        elif payload.emoji.name == "🔔":
            role = discord.utils.get(guild.roles, name="Announcements")
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("removed")

@client.command(pass_context=True, brief="Shows users balance", aliases=["bal"])
async def balance(ctx, member: discord.Member = None):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()

    if result_userID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
        db.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = QLS.fetchone()
    await ctx.send(f"{ctx.message.author.mention} has a balance of {result_userbal[0]} {C_NAME}")

@client.command(pass_context=True, aliases=["store"])
async def shop(ctx):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()

    if result_userID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
        db.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()
    embed = discord.Embed(title="The Shop", color=discord.Color.dark_grey())
    embed.add_field(name="Coach", value="Get 1 Basketball per hour", inline=False)
    embed.add_field(name="__**Your Rack**__", value=f"Basketballs: {result_userbal[0]} {C_NAME}", inline=False)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def buy(ctx):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()

    if result_userID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
        db.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()
    if amount > int(result_userbal[0]):
        await ctx.send(f"You don't have that many {C_NAME}")
        return

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()
    await ctx.send(f"{ctx.message.author.mention} now has {result_userbal} {C_NAME}")

@client.command(pass_context=True, brief="Pay Someone")
async def give(ctx, other: discord.Member, amount: int):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    OTHER_ID = other.id
    OTHER_NAME = str(other)

    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = SQL.fetchone()
    SQL.execute(f'select user_id from Accounts where user_id="{OTHER_ID}"')
    result_otherID = SQL.fetchone()

    if result_userID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, START_BALANCE))
        db.commit()
    if result_otherID is None:
        SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (OTHER_NAME, OTHER_ID, START_BALANCE))
        db.commit()

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = SQL.fetchone()
    if amount > int(result_userbal[0]):
        await ctx.send(f"{ctx.message.author.mention} does not have that many {C_NAME}")
        return

    SQL.execute('update Accounts set balance = balance - ? where user_id = ?', (amount, USER_ID))
    db.commit()
    SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (amount, OTHER_ID))
    db.commit()

    await ctx.send(f"{ctx.message.author.mention} sent {other.mention} {amount} {C_NAME}")


@client.command(pass_context=True, brief="list top 10 bank accounts", aliases=["top"])
async def top10(ctx):
    SQL.execute(f"select user_name, balance from Accounts order by balance desc")
    result_top10 = SQL.fetchmany(2)


    embed = discord.Embed(
        colour=discord.Colour.orange()
    )

    embed.set_author(name="Top 10 bank accounts")
    embed.add_field(name="#1", value=f"User: {result_top10[0][0]} Bal: {result_top10[0][1]}", inline=False)
    embed.add_field(name="#2", value=f"User: {result_top10[1][0]} Bal: {result_top10[1][1]}", inline=False)

    await ctx.send(embed=embed)



extension = ['cogs.help_command', 'cogs.General Commands', 'cogs.Fun Commands', 'cogs.mc', 'cogs.Suggestions', 'cogs.Application', 'cogs.Moderation', 'cogs.Administrator Commands', 'cogs.global']

if __name__ == '__main__':
    for ext in extension:
        client.load_extension(ext)

client.run('NzIxMzk3ODk2NzA0MTYzOTY1.XxIv2A.nsvzTq3ue_o45YRwk309ZUuYKV4')
