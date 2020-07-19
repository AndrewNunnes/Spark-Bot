import discord
from discord.ext import commands
import sqlite3
import aiosqlite
import os

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.SQL = None
        async with aiosqlite.connect(os.path.join(DIR, "BankAccounts.db")) as self.db:
            self.SQL = await self.db.cursor()
            self.START_BALANCE = 100
            self.C_NAME = "Basketballs"
DIR = os.path.dirname(__file__)

@commands.command(pass_context=True, brief="Shows users balance", aliases=["bal"])
async def balance(self, ctx, member: discord.Member = None):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    self.SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    self.SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = self.SQL.fetchone()

    if result_userID is None:
        self.SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, self.START_BALANCE))
        self.db.commit()

    self.SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = self.SQL.fetchone()
    await ctx.send(f"{ctx.message.author.mention} has a balance of {result_userbal[0]} {self.C_NAME}")

@commands.command(pass_context=True, aliases=["store"])
async def shop(self, ctx):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    self.SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    self.SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = self.SQL.fetchone()

    if result_userID is None:
        self.SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, self.START_BALANCE))
        self.db.commit()

    self.SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = self.SQL.fetchone()
    embed = discord.Embed(title="The Shop", color=discord.Color.dark_grey())
    embed.add_field(name="Coach", value="Get 1 Basketball per hour", inline=False)
    embed.add_field(name="__**Your Rack**__", value=f"Basketballs: {result_userbal[0]} {self.C_NAME}", inline=False)
    await ctx.send(embed=embed)

@commands.command(pass_context=True)
async def buy(self, ctx, amount: int):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    self.SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    self.SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = self.SQL.fetchone()

    if result_userID is None:
        self.SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, self.START_BALANCE))
        self.db.commit()

    self.SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = self.SQL.fetchone()
    if amount > int(result_userbal[0]):
        await ctx.send(f"You don't have that many {self.C_NAME}")
        return

    self.SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = self.SQL.fetchone()
    await ctx.send(f"{ctx.message.author.mention} now has {result_userbal} {self.C_NAME}")

@commands.command(pass_context=True, brief="Pay Someone")
async def give(self, ctx, other: discord.Member, amount: int):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    OTHER_ID = other.id
    OTHER_NAME = str(other)

    self.SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" real)')
    self.SQL.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
    result_userID = self.SQL.fetchone()
    self.SQL.execute(f'select user_id from Accounts where user_id="{OTHER_ID}"')
    result_otherID = self.SQL.fetchone()

    if result_userID is None:
        self.SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (USER_NAME, USER_ID, self.START_BALANCE))
        self.db.commit()
    if result_otherID is None:
        self.SQL.execute('insert into Accounts(user_name, user_id, balance) values(?,?,?)', (OTHER_NAME, OTHER_ID, self.START_BALANCE))
        self.db.commit()

    self.SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')
    result_userbal = self.SQL.fetchone()
    if amount > int(result_userbal[0]):
        await ctx.send(f"{ctx.message.author.mention} does not have that many {self.C_NAME}")
        return

    self.SQL.execute('update Accounts set balance = balance - ? where user_id = ?', (amount, USER_ID))
    self.db.commit()
    self.SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (amount, OTHER_ID))
    self.db.commit()

    await ctx.send(f"{ctx.message.author.mention} sent {other.mention} {amount} {self.C_NAME}")


@commands.command(pass_context=True, brief="list top 10 bank accounts", aliases=["top"])
async def top10(self, ctx):
    self.SQL.execute(f"select user_name, balance from Accounts order by balance desc")
    result_top10 = self.SQL.fetchmany(2)


    embed = discord.Embed(
        colour=discord.Colour.orange()
    )

    embed.set_author(name="Top 10 bank accounts")
    embed.add_field(name="#1", value=f"User: {result_top10[0][0]} Bal: {result_top10[0][1]}", inline=False)
    embed.add_field(name="#2", value=f"User: {result_top10[1][0]} Bal: {result_top10[1][1]}", inline=False)
    embed.add_field(name="#3", value=f"User: {result_top10[2][0]} Bal: {result_top10[2][2]}", inline=False)
    embed.add_field(name="#4", value=f"User: {result_top10[3][0]} Bal: {result_top10[3][3]}", inline=False)
    embed.add_field(name="#5", value=f"User: {result_top10[4][0]} Bal: {result_top10[4][4]}", inline=False)
    embed.add_field(name="#6", value=f"User: {result_top10[5][0]} Bal: {result_top10[5][5]}", inline=False)
    embed.add_field(name="#7", value=f"User: {result_top10[6][0]} Bal: {result_top10[6][6]}", inline=False)
    embed.add_field(name="#8", value=f"User: {result_top10[7][0]} Bal: {result_top10[7][7]}", inline=False)
    embed.add_field(name="#9", value=f"User: {result_top10[8][0]} Bal: {result_top10[8][8]}", inline=False)
    embed.add_field(name="#10", value=f"User: {result_top10[9][0]} Bal: {result_top10[9][9]}", inline=False)

    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))