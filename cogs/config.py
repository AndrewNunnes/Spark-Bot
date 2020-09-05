
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
        
        self.db = self.bot.get_cog('Database')
        
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
    
    @group(
        invoke_without_command=True, 
        brief="{Commands for Configuring Prefixes}", 
        usage="prefix", 
        aliases=['pre', 'pref'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    async def prefix(self, ctx):
        
        e = discord.Embed(
            description=f"__*Available Prefix Commands*__")
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        e.set_thumbnail(
            url=ctx.author.avatar_url)
      
        fields = [("• **prefix change :** `{ctx.prefix}prefix change <new_prefix>`", 
                  "{Change the Bot's Prefix}", False), 
                  
                  ("• **prefix reset :** `{ctx.prefix}prefix reset`", 
                  "{Reset the Custom Prefix}", False)]
        
        for n, v, i in fields:
            e.add_field(
                name=n, 
                value=v, 
                inline=i)
        
        await ctx.send(embed=e)
          
    @prefix.command(
        brief="{Change the Bot's Prefix}", 
        usage="prefix change <new_prefix>", 
        aliases=['new', 'switch'])
    @guild_only()
    @cooldown(1, 5, BucketType.user)
    @has_permissions(manage_guild=True)
    async def change(self, ctx, pre: str=None):
        
        redmark = "<:redmark:738415723172462723>"
        
        #Get the current prefix of the guild
        get_pre = await self.db.get_prefix(ctx.guild.id)
        
        #If a new prefix isn't said
        if not pre:
            return await ctx.send(f"The server prefix is set to `{get_pre}`. Use `{get_pre}config prefix` to change it")

        #If a new prefix is given
        else:
            if len(pre) > 5:
                e = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, prefix can't be longer than 5 characters in length", 
                    color=0x420000)
                await ctx.send(embed=e)
                return
            
            else:
                #Set the new prefix for this guild
                await self.db.set_prefix(ctx.guild.id, pre)
            
                await ctx.send(f"The server prefix has been set to `{pre}`. Use `{pre}config prefix <newprefix>` to change it again")
    
    @prefix.command(
        brief="{Reset the Prefix}", 
        usage="prefix reset", 
        aliases=['delete', 'del'])
    @guild_only()
    @cooldown(1, 2.5, BucketType.user)
    @has_permissions(manage_guild=True)
    async def reset(self, ctx):
        
        #Set the prefix to the default 
        #With out drop prefix function
        await self.db.drop_prefix(ctx.guild.id)
        
        await ctx.send(f"*The prefix has been reset to `?`!*")
    
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
      usage="config role")
    @guild_only()
    @has_permissions(manage_roles=True)
    @cooldown(1, 1.5, BucketType.user)
    async def role(self, ctx):
      
        cog = self.gc.get_cog_by_class('Role')

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
