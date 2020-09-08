
#•----------Modules----------•#
import discord

from discord.ext.commands import BucketType, cooldown, guild_only, bot_has_permissions, is_owner, group, Cog

from datetime import datetime

#•----------Class----------•#
class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
    
#•---------Functions----------•#
    
    #Used to get a cog by it's class name
    def get_cog_by_class(self, name):
        for cog in self.bot.cogs.values():
            if cog.__class__.__name__ == name:
                return cog

#•----------Commands----------•#
    
    @group(
        name="help", 
        invoke_without_command=True, 
        brief="{Help Menu, what else?}", 
        usage="help")
    @cooldown(1, 2.0, BucketType.user)
    @guild_only()
    async def kyrie(self, ctx):
        
        #Makes things shorter
        p = ctx.prefix

        #Gets the Cogs
        info = self.get_cog_by_class('Info')
        
        fun = self.get_cog_by_class('Fun')
        
        giveaway = self.get_cog_by_class('Giveaway')
        
        mod = self.get_cog_by_class('Moderation')
        
        misc = self.get_cog_by_class('Misc')

        owner = self.get_cog_by_class('Owner')
        
        #Make the embed
        e = discord.Embed(
            description="__**{{Category Index}}**__")
            
        #Make fields 
        fields = [
                  (f"📰 **{info.qualified_name}**", 
                  f"`{{{p}help info}}`", True), 
                  
                  (f"🎪 **{fun.qualified_name}**", 
                  f"`{{{p}help fun}}`", True), 
                  
                  #(f"🎉 **{giveaway.qualified_name}**", 
                  #f"`{{{p}help giveaway}}`", True), 
                  
                  (f"⚙️ **{mod.qualified_name}**", 
                  f"`{{{p}help mod}}`", True), 
                  
                  (f"🔐 **{owner.qualified_name}**", 
                  f"`{{{p}help owner}}`", True), 
                  
                  (f"🔗 **{misc.qualified_name}**", 
                  f"`{{{p}help misc}}`", True)]
                  
        #Add the fields      
        for n, v, i in fields:
            e.add_field(
                name=n, 
                value=v, 
                inline=i)
        
        e.set_thumbnail(
            url=ctx.author.avatar_url)

        e.set_footer(
            text=f"Requested by {ctx.author}")

        e.timestamp = datetime.utcnow()
        
        m = await ctx.send(embed=e)
    
    @kyrie.command(
        brief="{Commands for Info Category}", 
        usage="help info")
    @cooldown(1, 2.0, BucketType.user)
    @guild_only()
    @bot_has_permissions(add_reactions=True)
    async def info(self, ctx):

        garbage = "<:trash:734043301187158082>"
        redmark = "<:redmark:738415723172462723>"
        
        #Get the cog by it's class
        cog = self.get_cog_by_class('Info')
        
        #Get the commands and store as a variable
        c = cog.get_commands()

        #Split the commands into 2 pages
        first = c[:len(c)//2]
        second = c[len(c)//2:]

        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            title=cog.qualified_name, 
            description="*() - Optional\n<> - Required*", 
            timestamp=datetime.utcnow())
        
        for comm in first:
        
            fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.set_thumbnail(
            url=ctx.author.avatar_url)
        e.set_author(
            name=f"Page {cur_page}/{pages}")
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        
        #Store the first embed we're sending
        msg = await ctx.send(embed=e)
        
        #Reactions to add
        emotes = ['⬅️', '➡️', '⏹']
        for react in emotes:
            #Add the reactions
            await msg.add_reaction(react)
        
        #Custom check to check for the author of the command
        #And check for the right emojis
        #And check for the specific message
        def checkauth(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await msg.edit(embed=err)
                await msg.clear_reactions()
                break
              
            else:
                #Check for the specific emoji
                #And if the user isn't trying to go to the negative side 
                #Of pages
                if str(reaction.emoji) == '⬅️' and cur_page > 1:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page -= 1
                    
                    e = discord.Embed(
                        title=f"{cog.qualified_name}", 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in first:
        
                        fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                #Check for the specific emoji
                #And if the user tries to go forward too much
                elif str(reaction.emoji) == '➡️' and cur_page != pages:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page += 1
                    
                    e = discord.Embed(
                        title=cog.qualified_name, 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in second:
        
                        fields2 = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields2:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                    
                #Used to delete the embed
                elif str(reaction.emoji) == '⏹':
                    await msg.clear_reactions()
                    e = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    await msg.edit(embed=e, delete_after=5)
                
                else:
                    await msg.remove_reaction(reaction, user)

    @kyrie.command(
        brief="{Commands for Fun Category}", 
        usage="help fun")
    @cooldown(1, 2.0, BucketType.user)
    @bot_has_permissions(add_reactions=True)
    @guild_only()
    async def fun(self, ctx):

        garbage = "<:trash:734043301187158082>"
        redmark = "<:redmark:738415723172462723>"
        
        #Get the cog by it's class
        cog = self.get_cog_by_class('Fun')
        
        #Get the commands and store as a variable
        c = cog.get_commands()

        #Split the commands into 2 pages
        first = c[:len(c)//2]
        second = c[len(c)//2:]

        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            title=cog.qualified_name, 
            description="*() - Optional\n<> - Required*", 
            timestamp=datetime.utcnow())
        
        for comm in first:
        
            fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.set_thumbnail(
            url=ctx.author.avatar_url)
        e.set_author(
            name=f"Page {cur_page}/{pages}")
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        
        #Store the first embed we're sending
        msg = await ctx.send(embed=e)
        
        #Reactions to add
        emotes = ['⬅️', '➡️', '⏹']
        for react in emotes:
            #Add the reactions
            await msg.add_reaction(react)
        
        #Custom check to check for the author of the command
        #And check for the right emojis
        #And check for the specific message
        def checkauth(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await msg.edit(embed=err)
                await msg.clear_reactions()
                break
              
            else:
                #Check for the specific emoji
                #And if the user isn't trying to go to the negative side 
                #Of pages
                if str(reaction.emoji) == '⬅️' and cur_page > 1:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page -= 1
                    
                    e = discord.Embed(
                        title=f"{cog.qualified_name}", 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in first:
        
                        fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                #Check for the specific emoji
                #And if the user tries to go forward too much
                elif str(reaction.emoji) == '➡️' and cur_page != pages:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page += 1
                    
                    e = discord.Embed(
                        title=cog.qualified_name, 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in second:
        
                        fields2 = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields2:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                    
                #Used to delete the embed
                elif str(reaction.emoji) == '⏹':
                    await msg.clear_reactions()
                    e = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    await msg.edit(embed=e, delete_after=5)
                
                else:
                    await msg.remove_reaction(reaction, user)

    @kyrie.command(
        brief="{Commands for Giveaway Category}", 
        usage="help giveaway")
    @cooldown(1, 2.0, BucketType.user)
    @is_owner()
    @bot_has_permissions(add_reactions=True)
    @guild_only()
    async def giveaway(self, ctx):

        garbage = "<:trash:734043301187158082>"
        redmark = "<:redmark:738415723172462723>"
        
        #Get the cog by it's class
        cog = self.get_cog_by_class('Giveaway')
        
        #Get the commands and store as a variable
        c = cog.get_commands()

        #Split the commands into 2 pages
        first = c[:len(c)//2]
        second = c[len(c)//2:]

        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            title=cog.qualified_name, 
            description="*() - Optional\n<> - Required*", 
            timestamp=datetime.utcnow())
        
        for comm in first:
        
            fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.set_thumbnail(
            url=ctx.author.avatar_url)
        e.set_author(
            name=f"Page {cur_page}/{pages}")
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        
        #Store the first embed we're sending
        msg = await ctx.send(embed=e)
        
        #Reactions to add
        emotes = ['⬅️', '➡️', '⏹']
        for react in emotes:
            #Add the reactions
            await msg.add_reaction(react)
        
        #Custom check to check for the author of the command
        #And check for the right emojis
        #And check for the specific message
        def checkauth(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await msg.edit(embed=err)
                await msg.clear_reactions()
                break
              
            else:
                #Check for the specific emoji
                #And if the user isn't trying to go to the negative side 
                #Of pages
                if str(reaction.emoji) == '⬅️' and cur_page > 1:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page -= 1
                    
                    e = discord.Embed(
                        title=f"{cog.qualified_name}", 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in first:
        
                        fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                #Check for the specific emoji
                #And if the user tries to go forward too much
                elif str(reaction.emoji) == '➡️' and cur_page != pages:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page += 1
                    
                    e = discord.Embed(
                        title=cog.qualified_name, 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in second:
        
                        fields2 = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields2:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                    
                #Used to delete the embed
                elif str(reaction.emoji) == '⏹':
                    await msg.clear_reactions()
                    e = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    await msg.edit(embed=e, delete_after=5)
                
                else:
                    await msg.remove_reaction(reaction, user)

    @kyrie.command(
        brief="{Commands for Moderation Category}", 
        usage="help mod")
    @cooldown(1, 2.0, BucketType.user)
    @bot_has_permissions(add_reactions=True)
    @guild_only()
    async def mod(self, ctx):

        garbage = "<:trash:734043301187158082>"
        redmark = "<:redmark:738415723172462723>"
        
        #Get the cog by it's class
        cog = self.get_cog_by_class('Moderation')
        
        #Get the commands and store as a variable
        c = cog.get_commands()

        #Split the commands into 2 pages
        first = c[:len(c)//2]
        second = c[len(c)//2:]

        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            title=cog.qualified_name, 
            description="*() - Optional\n<> - Required*", 
            timestamp=datetime.utcnow())
        
        for comm in first:
        
            fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.set_thumbnail(
            url=ctx.author.avatar_url)
        e.set_author(
            name=f"Page {cur_page}/{pages}")
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        
        #Store the first embed we're sending
        msg = await ctx.send(embed=e)
        
        #Reactions to add
        emotes = ['⬅️', '➡️', '⏹']
        for react in emotes:
            #Add the reactions
            await msg.add_reaction(react)
        
        #Custom check to check for the author of the command
        #And check for the right emojis
        #And check for the specific message
        def checkauth(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await msg.edit(embed=err)
                await msg.clear_reactions()
                break
              
            else:
                #Check for the specific emoji
                #And if the user isn't trying to go to the negative side 
                #Of pages
                if str(reaction.emoji) == '⬅️' and cur_page > 1:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page -= 1
                    
                    e = discord.Embed(
                        title=f"{cog.qualified_name}", 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in first:
        
                        fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                #Check for the specific emoji
                #And if the user tries to go forward too much
                elif str(reaction.emoji) == '➡️' and cur_page != pages:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page += 1
                    
                    e = discord.Embed(
                        title=cog.qualified_name, 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in second:
        
                        fields2 = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields2:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                    
                #Used to delete the embed
                elif str(reaction.emoji) == '⏹':
                    await msg.clear_reactions()
                    e = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    await msg.edit(embed=e, delete_after=5)
                
                else:
                    await msg.remove_reaction(reaction, user)

    @kyrie.command(
        brief="{Commands for Owner Category}", 
        usage="help owner")
    @cooldown(1, 2.0, BucketType.user)
    @bot_has_permissions(add_reactions=True)
    @guild_only()
    async def owner(self, ctx):

        garbage = "<:trash:734043301187158082>"
        redmark = "<:redmark:738415723172462723>"
        
        #Get the cog by it's class
        cog = self.get_cog_by_class('Owner')
        
        #Get the commands and store as a variable
        c = cog.get_commands()

        #Split the commands into 2 pages
        first = c[:len(c)//2]
        second = c[len(c)//2:]

        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            title=cog.qualified_name, 
            description="*() - Optional\n<> - Required*", 
            timestamp=datetime.utcnow())
        
        for comm in first:
        
            fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.set_thumbnail(
            url=ctx.author.avatar_url)
        e.set_author(
            name=f"Page {cur_page}/{pages}")
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        
        #Store the first embed we're sending
        msg = await ctx.send(embed=e)
        
        #Reactions to add
        emotes = ['⬅️', '➡️', '⏹']
        for react in emotes:
            #Add the reactions
            await msg.add_reaction(react)
        
        #Custom check to check for the author of the command
        #And check for the right emojis
        #And check for the specific message
        def checkauth(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await msg.edit(embed=err)
                await msg.clear_reactions()
                break
              
            else:
                #Check for the specific emoji
                #And if the user isn't trying to go to the negative side 
                #Of pages
                if str(reaction.emoji) == '⬅️' and cur_page > 1:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page -= 1
                    
                    e = discord.Embed(
                        title=f"{cog.qualified_name}", 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in first:
        
                        fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                #Check for the specific emoji
                #And if the user tries to go forward too much
                elif str(reaction.emoji) == '➡️' and cur_page != pages:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page += 1
                    
                    e = discord.Embed(
                        title=cog.qualified_name, 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in second:
        
                        fields2 = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields2:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                    
                #Used to delete the embed
                elif str(reaction.emoji) == '⏹':
                    await msg.clear_reactions()
                    e = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    await msg.edit(embed=e, delete_after=5)
                
                else:
                    await msg.remove_reaction(reaction, user)

    @kyrie.command(
        brief="{Commands for Misc Category}", 
        usage="help misc")
    @cooldown(1, 2.0, BucketType.user)
    @bot_has_permissions(add_reactions=True)
    @guild_only()
    async def misc(self, ctx):

        garbage = "<:trash:734043301187158082>"
        redmark = "<:redmark:738415723172462723>"
        
        #Get the cog by it's class
        cog = self.get_cog_by_class('Misc')
        
        #Get the commands and store as a variable
        c = cog.get_commands()

        #Split the commands into 2 pages
        first = c[:len(c)//2]
        second = c[len(c)//2:]

        #Max pages we want for this embed
        pages = 2
        #The current page we're on
        #Defaults to 0
        cur_page = 1
        
        e = discord.Embed(
            title=cog.qualified_name, 
            description="*() - Optional\n<> - Required*", 
            timestamp=datetime.utcnow())
        
        for comm in first:
        
            fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
            for n, v, i in fields:
                e.add_field(
                    name=n, 
                    value=v, 
                    inline=i)
        
        e.set_thumbnail(
            url=ctx.author.avatar_url)
        e.set_author(
            name=f"Page {cur_page}/{pages}")
        
        e.set_footer(
            text=f"Requested by {ctx.author}")
        
        #Store the first embed we're sending
        msg = await ctx.send(embed=e)
        
        #Reactions to add
        emotes = ['⬅️', '➡️', '⏹']
        for react in emotes:
            #Add the reactions
            await msg.add_reaction(react)
        
        #Custom check to check for the author of the command
        #And check for the right emojis
        #And check for the specific message
        def checkauth(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['⬅️', '➡️', '⏹']
        
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=180.0, check=checkauth)
            
            #If user takes too long to react
            except asyncio.TimeoutError:
                err = discord.Embed(
                    description=f"{redmark} __*{ctx.author.mention}, you took too long to react*__", 
                    color=0x420000)
                await msg.edit(embed=err)
                await msg.clear_reactions()
                break
              
            else:
                #Check for the specific emoji
                #And if the user isn't trying to go to the negative side 
                #Of pages
                if str(reaction.emoji) == '⬅️' and cur_page > 1:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page -= 1
                    
                    e = discord.Embed(
                        title=f"{cog.qualified_name}", 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in first:
        
                        fields = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                #Check for the specific emoji
                #And if the user tries to go forward too much
                elif str(reaction.emoji) == '➡️' and cur_page != pages:
                    await msg.remove_reaction(reaction, user)
                    
                    cur_page += 1
                    
                    e = discord.Embed(
                        title=cog.qualified_name, 
                        description="*() - Optional\n<> - Required*", 
                        timestamp=datetime.utcnow())
                    e.set_thumbnail(
                        url=ctx.author.avatar_url)

                    for comm in second:
        
                        fields2 = [(f"• **{comm.name} :** `{ctx.prefix}{comm.usage}`", comm.brief, False)]
        
                        for n, v, i in fields2:
                            e.add_field(
                                name=n, 
                                value=v, 
                                inline=i)

                    e.set_author(
                        name=f"Page {cur_page}/{pages}")
                    
                    e.set_footer(
                        text=f"Requested by {ctx.author}")
                    
                    await msg.edit(embed=e)
                    
                #Used to delete the embed
                elif str(reaction.emoji) == '⏹':
                    await msg.clear_reactions()
                    e = discord.Embed(
                        description=f"{garbage} __*Removing this embed in 5 seconds...*__", 
                        color=0x420000)
                    await msg.edit(embed=e, delete_after=5)
                
                else:
                    await msg.remove_reaction(reaction, user)

#•----------Setup/Add this Cog----------•#
def setup(bot):
    bot.add_cog(Help(bot))
