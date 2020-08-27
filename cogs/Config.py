
#•----------Modules----------•#
import discord

from discord.ext.commands import group, has_permissions, bot_has_permissions, guild_only, \
BucketType, Greedy, Cog, cooldown

from datetime import datetime

from typing import Optional

import cogs._json

#•----------Class-----------•#
class Config(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.gc = self.bot.get_cog('Helpdude')
        
#•------------Subcommands-----------•#

    @group(
        invoke_without_command=True, 
        brief="{Configuration Menu/Commands}", 
        usage="config")
    @has_permissions(manage_messages=True)
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def config(self, ctx):

        cog = self.gc.get_cog_by_class('Config')
        
        e = discord.Embed(
          title=f"__*{cog.qualified_name}*__\n*() - Optional\n<> - Required*")
          
        #Iterate through this cog's commands
        for c in cog.walk_commands():
            
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
                    
        e.timestamp = datetime.utcnow()
        e.set_author(
            name=f"Requested by {ctx.author}")
        
        await ctx.send(embed=e)
          
    @config.command(
      brief="{Change the Bot's Prefix}", 
      usage="prefix <new_prefix>")
    @guild_only()
    @cooldown(1, 5, BucketType.user)
    @has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, pre: str):
        data = cogs._json.read_json('prefixes')
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, 'prefixes')
        
        #If a new prefix isn't said
        if not pre:
            await ctx.send(f"The server prefix is set to {ctx.prefix}. Use {ctx.prefix}prefix to change it")
        
        #If a new prefix is given
        else:
            await ctx.send(f"The server prefix has been set to `{pre}`. Use `{pre}prefix <newprefix>` to change it again")

#•----------Command Menus----------•#
#•--{Gets the cogs and Show their Commands--•#

    @config.command(
        brief="{Menu for Welcome Messages}", 
        usage="config wcmenu", 
        aliases=['wlcmemu', 'welcomemenu']
    )
    @guild_only()
    @has_permissions(manage_channels=True)
    @cooldown(1, 1.5, BucketType.user)
    async def wcmenu(self, ctx):
        
        #Get the Welcome Cog
        cog = self.gc.get_cog_by_class('Welcome')
        
        #Make the embed
        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            color=0x420000)
        
        #Iterate through all (sub)commands 
        #For the cog we get
        for c in cog.walk_commands():
            
            #Make our fields
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.brief}`", f"{c.usage}", True)]
            
            #Iterate through our fields list
            for n, v, i in fields:
                #Add the fields
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
                    
        e.timestamp = datetime.utcnow()
        e.set_author(
            name=f"Requested by {ctx.author}")
        
        await ctx.send(embed=e)

    @config.command(
        brief="{Menu for Goodbye Messages}", 
        usage="config gbmenu", 
        aliases=['byemenu', 'goodbyemenu']
    )
    @guild_only()
    @has_permissions(manage_channels=True)
    @cooldown(1, 1.5, BucketType.user)
    async def gbmenu(self, ctx):

        cog = self.gc.get_cog_by_class('Goodbye')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            color=0x420000)
        
        for c in cog.walk_commands():
            
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.brief}`", f"{c.usage}", True)]
            
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
        e.timestamp = datetime.utcnow()
        e.set_author(
            name=f"Requested by {ctx.author}")
    
        await ctx.send(embed=e)
    
    @config.command(
        brief="{Menu for Logging}", 
        usage="config logsmenu", 
        aliases=['logmenu'])
    @has_permissions(manage_messages=True)
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    async def logsmenu(self, ctx):

        cog = self.gc.get_cog_by_class('Logging')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__",
            color=0x420000)
        
        #Iterate through all commands including subcommands 
        #Inside of that cog
        for c in cog.walk_commands():
            
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
            
        e.timestamp = datetime.utcnow()
        e.set_footer(
            name=f"Requested by {ctx.author}")
        
        await ctx.send(embed=e)

    @config.command(
      brief="{Menu for Role Management}", 
      usage="role")
    @guild_only()
    @has_permissions(manage_roles=True)
    @cooldown(1, 1.5, BucketType.user)
    async def role(self, ctx):
      
        cog = self.gc.get_cog_by_class('Role Management')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__",
            color=0x420000)
      
        for c in cog.walk_commands():
          
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            for name, val, i in fields:
                e.add_field(
                    name=name, 
                    value=val, 
                    inline=i)
        
        e.timestamp = datetime.utcnow()
        e.set_author(
            name=f"Requested by {ctx.author}")
      
        await ctx.send(embed=e)
      
    @config.command(
      brief="{Menu for Managing Categories}", 
      usage="config category", 
      aliases=['categ'])
    @guild_only()
    @cooldown(1, 1.5, BucketType.user)
    @has_permissions(manage_channels=True)
    async def category(self, ctx):
      
        cog = self.gc.get_cog_by_class('Category')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            color=0x420000)
            
        for c in cog.walk_commands():
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.timestamp = datetime.utcnow()
        
        e.set_author(
            name=f"Requested by {ctx.author}")
      
        await ctx.send(embed=e)
      
    @config.command(
      brief="{Menu for Managing Channels}", 
      usage="config channel", 
      aliases=['chmenu', 'channels', 'chann'])
    @guild_only()
    @has_permissions(manage_channels=True)
    @cooldown(1, 1.5, BucketType.user)
    async def channel(self, ctx):
      
        cog = self.gc.get_cog_by_class('Channels')

        e = discord.Embed(
            title=f"__*{cog.qualified_name}*__\n_*() - Optional\n<> - Required*_\n\n__*Your Available Commands*__", 
            color=0x420000)
        
        for c in cog.walk_commands():
            fields = [(f"• **{c.name} :** `{ctx.prefix}{c.usage}`", f"{c.brief}", True)]
            
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.timestamp = datetime.utcnow()
        
        await ctx.send(embed=e)

#•----------Setup/Add this Cog----------•#
def setup(bot):
    bot.add_cog(Config(bot))
