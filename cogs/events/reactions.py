import discord
from discord.ext import commands
from discord.utils import get

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Role Reactions for Announcements/Giveaways
    @commands.Cog.listener()
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

    @commands.Cog.listener()
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
                    
    #Role Reaction for New Members(Verified Member)
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.guild_id or payload.member.bot:
            return
        if payload.message_id != 729493725717332021:
            return
        elif payload.message_id != 737848544852967445:
            return
        
        role = discord.utils.get(payload.member.guild.roles, name=['Verified Member' or '{Member}'])
        if not role:
            return
        
        else:
            if payload.emoji.name == '🏀':
                await payload.member.add_roles(role)
                embed = discord.Embed(title="Welcome to the server", description=f"You've now been verified\n\nTo see my available commands type in `{prefix}help` in #bot-commands. If you have any questions make sure to ask the Owner\nEnjoy your stay 🙂", color=discord.Color.dark_blue())
                await payload.member.send(embed=embed)
                print("Now verified")

def setup(bot):
    bot.add_cog(Reactions(bot))
