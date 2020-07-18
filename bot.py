import discord
from discord.ext import commands
import random
from random import randint
import platform
import logging
import asyncio
import datetime
import typing

client = commands.Bot(command_prefix = '!', case_insensitive=True)
client.remove_command('help')

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



extension = ['cogs.help_command', 'cogs.General_Commands', 'cogs.Fun_Commands', 'cogs.mc', 'cogs.Application', 'cogs.Suggestions', 'cogs.Moderation', 'cogs.Administrator_Commands', 'cogs.global']

if __name__ == '__main__':
    for ext in extension:
        client.load_extension(ext)

client.run('token')
