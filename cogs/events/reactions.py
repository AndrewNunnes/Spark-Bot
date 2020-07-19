import discord
from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Role Reactions
    @commands.Cog.listener
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 733354307298132078:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == "🎉":
                role = discord.utils.get(guild.roles, name="Giveaway")
            elif payload.emoji.name == "🔔":
                role = discord.utils.get(guild.roles, name="Announcements")
            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print("done")

    @commands.Cog.listener
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 733354307298132078:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == "🎉":
                role = discord.utils.get(guild.roles, name="Giveaway")
            elif payload.emoji.name == "🔔":
                role = discord.utils.get(guild.roles, name="Announcements")
            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print("removed")

def setup(bot):
    bot.add_cog(Reactions(bot))