import discord
from discord.ext import commands
import asyncio
import logging

logging.basicConfig(level = logging.INFO)

class Help_Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Creates A New Help Command


    @commands.command()
    @commands.guild_only()
    async def help(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        
        member = ctx.author if not member else member
        
        embed = discord.Embed(
            title=f'All Commands (Default prefix is `{ctx.prefix}`)',
            description="__**{{Command Index}}**__",
            color=discord.Color.darker_grey())
        
        embed.add_field(name="📖 Main Menu", value="`Shows this Menu`", inline=True)
        embed.add_field(name="♠️ General Category", value="`List of General Commands`", inline=True)
        embed.add_field(name="<:fun:734648757441921124> Fun Category", value="`List of General Fun Commands`", inline=True)
        embed.add_field(name="<:grass:734647227523268668> Minecraft Category", value="`Fun Commands Related to Minecraft`", inline=True)
        embed.add_field(name="🎉 Giveaway Category", value="`List of Commands Related to Hosting Giveaways`", inline=True)
        embed.add_field(name="📚 Application/Suggestion Category", value="`List of Application/Suggestion Commands`", inline=True)
        #embed.add_field(name="📑 Application Category", value="`List of Application Commands`", inline=True)
        #embed.add_field(name="📫 Suggestion Category", value="`List of Suggestion Commands`", inline=True)
        embed.add_field(name="🔐 Moderation Category", value="`Commands Used to Moderate the Server`", inline=True)
        embed.add_field(name="😱 Roles Category", value="`Commands Used to Manage the Roles in the Server`", inline=True)
        embed.add_field(name="🔗 Misc Category", value="`Miscallaneous Commands`", inline=True)
        embed.add_field(name="<:trash:734043301187158082> Cancellation", value="`Deletes this Embed/Help Message`", inline=True)
        
        embed.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        
        embed.set_footer(text="{{Please Remember This Bot Is Not 100% Finished Yet}}")
        
        m = await ctx.send(embed=embed)
        await m.edit(embed=embed)
        await m.add_reaction('📖')
        await m.add_reaction('♣️')
        await m.add_reaction('<:fun:734648757441921124>')
        await m.add_reaction('<:grass:734647227523268668>')
        await m.add_reaction('🎉')
        await m.add_reaction('📚')
        await m.add_reaction('🔐')
        await m.add_reaction('😱')
        await m.add_reaction('🔗')
        await m.add_reaction('<:trash:734043301187158082>')
        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📖', '♣️', '<:fun:734648757441921124>', '<:grass:734647227523268668>', '🎉', '🔐','📚', '😱', '🔗', '<:trash:734043301187158082>']
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=45.0, check=checkreact)

            except asyncio.TimeoutError:
                bruh = discord.Embed(color=discord.Color.darker_grey())
                bruh.add_field(name="__**What were you doing?**__", value="You took too long to react with an emoji bruh 🤦🏽")
                bruh.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                await m.edit(embed=bruh)
            else:
                if str(reaction.emoji) == '🎉':
                    await m.remove_reaction('🎉', member)
                    
                    bruh = discord.Embed(
                      title=f'Giveaway Category  (Default prefix is `{ctx.prefix}`)', 
                      description="_*() - Optional\n<> - Required*_", 
                      color=0x919234)
                    
                    bruh.add_field(name="_*giveaway*_", value=f"{{`{ctx.prefix}giveaway`}}", inline=True)
                    bruh.add_field(name="_*end(gend, endgiveaway)*_", 
                    value=f"{{`{ctx.prefix}end <themessageid>`}}", 
                    inline=True)
                    
                    bruh.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    
                    await m.edit(embed=bruh)
                    
                elif str(reaction.emoji) == '😱':
                    await m.remove_reaction('😱', member)
                    
                    roleembed = discord.Embed(
                      title=f'Role Category (Default prefix is `{ctx.prefix}`)', 
                      description="_*() - Optional\n<> - Required*_", 
                      color=0x248298)
                      
                    roleembed.add_field(name="_*addrole {Give somebody a role*_", value=f"{{`{ctx.prefix}addrole <@user Rolename>`}}", inline=True)
                    roleembed.add_field(name="_*removerole {Remove somebody's role}*_", value=f"{{`{ctx.prefix}removerole <@user Rolename>`}}", inline=True)
                    roleembed.add_field(name="_*roleinfo {Info on a Role}*_", value=f"{{`{ctx.prefix}roleinfo <rolename>`}}", inline=True)
                    roleembed.add_field(name="_*rolelist {List of Roles in the Guild}*_", value=f"{{`{ctx.prefix}rolelist`}}", inline=True)
                    roleembed.add_field(name="_*roleperms {Perms on a Role}*_", value=f"{{`{ctx.prefix}roleperms <rolename>`}}", inline=True)
                    roleembed.add_field(name="_*(**Testing**)createrole {Creates a New Role}*_", value=f"{{`{ctx.prefix}createrole <rolename>`}}", inline=True)
                    roleembed.add_field(name="_*deleterole {Deletes a Role}*_", value=f"{{`{ctx.prefix}deleterole <rolename>`}}", inline=True)
                    
                    roleembed.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=roleembed)
                    
                elif str(reaction.emoji) == '♣️':
                    await m.remove_reaction('♣️', member)
                    
                    embed1 = discord.Embed(
                      title=f'General Category (Default prefix is `{ctx.prefix}`)', 
                      description="_*() - Optional\n<> - Required*_", 
                      color=discord.Color.darker_grey())

                    #embed1.add_field(name="__**Commands:**__", value="_*binfo*_ - {Shows info about the Bot}\n\n_*sinfo*_ - {Shows info about the server}\n\n_*uinfo*_ - {Shows info about a user}\n\n_*avatar*_ - {Shows the avatar of a user}\n\n_*ping*_ - {Runs a connection test to Discord}\n\n_*boosters*_ - {List of Boosters}", inline=True)
                    embed1.add_field(name="_*binfo {Info on the Bot}*_", value=f"{{`{ctx.prefix}binfo`}}", inline=True)
                    embed1.add_field(name="_*sinfo {Info on the Server}*_", value=f"{{`{ctx.prefix}sinfo`}}", inline=True)
                    embed1.add_field(name="_*uinfo {Info on you or a User}*_", value=f"{{`{ctx.prefix}uinfo (@user/userid)", inline=True)
                    embed1.add_field(name="_*ping {Connection Test to Discord}*_", value=f"{{`{ctx.prefix}ping`}}", inline=True)
                    embed1.add_field(name="_*boosters {See who boosted this server}*_", value=f"{{`{ctx.prefix}boosters`}}")
                    
                    embed1.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=embed1)
            
                elif str(reaction.emoji) == '<:fun:734648757441921124>':
                    await m.remove_reaction('<:fun:734648757441921124>', member)
                    embed = discord.Embed(
                      title=f'Fun Category (Default prefix is `{ctx.prefix}`)', 
                      description="_*() - Optional\n<> - Required*_", 
                      color=discord.Color.dark_blue())
                    
                    embed.add_field(name="_*8ball {Ask a question and get a response*_", value=f"{{`{ctx.prefix}8ball <question>`}}", inline=True)
                    embed.add_field(name="_*letschat/chat {Chat with the bot}*_", value=f"{{`{ctx.prefix}letschat/chat <yoursentence>`}}", inline=True)
                    embed.add_field(name="_*fact {Get a random fact}*_", value=f"{{`{ctx.prefix}fact`}}", inline=True)
                    embed.add_field(name="_*spotify {See who's listening to Spotify}*_", value=f"{{`{ctx.prefix}spotify (@member)`}}", inline=True)
                    embed.add_field(name="_*insta {Info on Insta Account}*_", value=f"{{`{ctx.prefix}insta <insta_user_name>`}}", inline=True)
                    embed.add_field(name="_*meme {Random Meme}*_", value=f"{{`{ctx.prefix}meme`}}", inline=True)
                    embed.add_field(name="_*gay {See how gay you are}*_", value=f"{{`{ctx.prefix}gay`}}", inline=True)
                    embed.add_field(name="_*penis {See how big your penis is}*_", value=f"{{`{ctx.prefix}penis`}}", inline=True)
                    embed.add_field(name="_*thot {See how much of a thot you are}*_", value=f"{{`{ctx.prefix}thot`}}", inline=True)
                    
                    embed.add_field(name="_*iq {What's your IQ?}*_", value=f"{{`{ctx.prefix}iq`}}", inline=True)
                    embed.add_field(name="_*hack {Hack Somebody}*_", value=f"{{`{ctx.prefix}hack <@user>`}}", inline=True)
                    embed.add_field(name="_*embed {Make your message a Fancy Embed}*_", value=f"{{`{ctx.prefix}embed <message_here>`}}", inline=True)
                    embed.add_field(name="_*add {Add two numbers}*_", value=f"{{`{ctx.prefix}add <numbers_here>`}}", inline=True)
                    embed.add_field(name="_*playb(playball) {Will you win a Basketball Game?}*_", value=f"{{`{ctx.prefix}playb/playball`}}", inline=True)
                    embed.add_field(name="_*punch {Punch a User}*_",value=f"{{`{ctx.prefix}punch <member> (reason)`}}", inline=True)
                    embed.add_field(name="_*slap {Slap a User}*_", value=f"{{`{ctx.prefix}slap <member> (reason)`}}", inline=True)
                    embed.add_field(name="_*hug {Hug a User}*_", value=f"{{`{ctx.prefix}hug <member>`}}", inline=True)
                    
                    embed.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")

                    #embed.add_field(name="_*bottles*_(!bottles 7 water) - {x bottles of x on the wall}\n\n_*hug*_ - {Hug someone}\n\n_*punch*_ - {Punch somebody}\n\n_*slap*_ - {Slap someone}\n\n_*coinflip*_ - {Flip a coin}", inline=True)
                    await m.edit(embed=embed)

                elif str(reaction.emoji) == '<:grass:734647227523268668>':
                    await m.remove_reaction('<:grass:734647227523268668>', member)
                    embed = discord.Embed(title=f'Minecraft Category (Default prefix is "{ctx.prefix}")', 
                    description="_*() - Optional\n<> - Required*_", 
                    color=0xa0722a)
                    
                    embed.add_field(name="_*skin {Get a users skin}*_", 
                    value=f"{{`{ctx.prefix}skin <username>`}}", inline=True)
                    embed.add_field(name="_*uuid {Get a Users uuid}*_", 
                    value=f"{{`{ctx.prefix}uuid <username>`}}", inline=True)
                    embed.add_field(name="_*getplayer {Get a username with uuid}*_", 
                    value=f"{{`{ctx.prefix}getplayer <uuid>`}}", inline=True)
                    embed.add_field(name="_*mcping {See the info on a server}*_", 
                    value=f"{{`{ctx.prefix}mcping <serverip>`}}", inline=True)
                    embed.add_field(name="_*mcsales {Minecraft Total Sales}*_", 
                    value=f"{{`{ctx.prefix}mcsales`}}", inline=True)
                    embed.add_field(name="_*buildidea {Get a random build idea}*_", 
                    value=f"{{`{ctx.prefix}buildidea`}}", inline=True)
                    embed.add_field(name="_*colorcodes {Minecraft Color Codes}*_", 
                    value=f"{{`{ctx.prefix}colorcodes`}}", inline=True)
                    
                    embed.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")

                    #embed.add_field(name="__**Commands:**__ ", value="_*mcping(!mcping play.hypixel.net)*_ - {Shows stats of a Minecraft server}\n\n_*skin*_ - {Get the skin of another P*mcsales*buildidea*_ - {Get a random build idea}\n\n_*colorcodes*_ - {Get the colorcodes of Minecraft Text}", inline=True)
                    await m.edit(embed=embed)

            
                elif str(reaction.emoji) == '📚':
                    await m.remove_reaction('📚', member)
                    embed4 = discord.Embed(title=f'Application/Suggestion Category (Default prefix is `{ctx.prefix}`)', color=0x223ba3)

                    embed4.add_field(name="_*applymod {Apply for Mod}*_", value=f"{{`{ctx.prefix}applymod`}}", inline=True)
                    embed4.add_field(name="_*suggest {Leave a Suggestion}*_", value=f"{{`{ctx.prefix}suggest <suggestion>`}}", inline=True)
                    
                    embed4.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=embed4)

                #elif str(reaction.emoji) == '📫':
                    #await m.remove_reaction('📫', member)
                    #embed5 = discord.Embed(title=f'Suggestion Commands (Default prefix is "{ctx.prefix}")', color=0x223ba3)

                    #embed5.add_field(name="__**Commands:**__", value="_*suggest*_ - {Leave a suggestion}", inline=True)
                    #await m.edit(embed=embed5)
                    
                elif str(reaction.emoji) == '<:trash:734043301187158082>':
                    await m.remove_reaction('<:trash:734043301187158082>', member)
                    garb = discord.Embed(color=discord.Color.darker_grey())
                    garb.add_field(name="Removing this embed...", value="Your decision but aight 🤷🏽\n\n<:trash:734043301187158082>Removing the embed in 5 seconds...<:trash:734043301187158082>")
                    
                    await m.edit(embed=garb, delete_after=5)

                elif str(reaction.emoji) == '🔐':
                    await m.remove_reaction('🔐', member)
                    embed = discord.Embed(
                      title=f'Moderation Category (Mods and above **Only**) (Default prefix is "{ctx.prefix}")', 
                      description="_*() - Optional\n<> - Required*_", 
                      color=0x9a9a23)
                    
                    embed.add_field(name="_*prefix {Change the Prefix of the Guild}*_", value=f"{{`{ctx.prefix}prefix <new_prefix>`}}", inline=True)
                    embed.add_field(name="_*kick {Kicks a Member from the Guild}*_", value=f"{{`{ctx.prefix}kick <themember>`}}", inline=True)
                    embed.add_field(name="_*ban {Bans a User from the Guild}*_", value=f"{{`{ctx.prefix}ban <member>`}}", inline=True)
                    embed.add_field(name="_*unban {Unbans a User from the Guild}*_", value=f"{{`{ctx.prefix}unban <User#1234>`}}", inline=True)
                    #embed.add_field(name="_*mute {Mutes a Member for a Specified Amount of Time}*_", value=f"{{`{ctx.prefix}mute <time>`}}", inline=True)
                    #embed.add_field(name="_*unmute {Unmuted a User Manually}*_", value=f"{{`{ctx.prefix}unmute <user>`}}", inline=True)
                    embed.add_field(name="_*purge(prune, clean) {Deletes a Specified Number of Messages}*_",value=f"{{`{ctx.prefix}purge/clean/prune <amount>`}}", inline=True)

                    #embed.add_field(name="__**Commands:**__", value="_*prefix*_ - {Change the Prefix of the server}\n\n_*kick*_ - {Kicks a User}\n\n_*ban*_ - {Bans a User}\n\n_*unban*_(!unban User name#1234) - {Unbans a User}\n\n_*mute*_ - {Mutes a user from texting for a specified amount of time}\n\n_*unmute*_ - {Manually Unmutes a User}\n\n_*purge(prune, clean)*_ - {Deletes a specified amount of messages}", inline=True)
                    
                    embed.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=embed)

                elif str(reaction.emoji) == '🔗':
                    await m.remove_reaction('🔗', member)
                    embed = discord.Embed(title=f'Misc Commands(Mods and Admins **Only**) (Default prefix is "{ctx.prefix}")', color=0x62239a)
                    
                    embed.add_field(name="_*createinvite {Creates a Pernament Invite Link}*_", value=f"{{`{ctx.prefix}createinvite <#channel_name>`}}", inline=True)
                    embed.add_field(name="_*invite {Invite the Bot to your Guild}*_", value=f"{{`{ctx.prefix}invite`}}", inline=True)
                    embed.add_field(name="_*announce {Bot will repeat your message}*_", value=f"{{`{ctx.prefix}announce <your_message>`}}", inline=True)
                    embed.add_field(name="_*dm {DM a Specified User}*_", value=f"{{`{ctx.prefix}dm <user> <message>`}}", inline=True)
                    embed.add_field(name="_*poll {Creates a Poll Interactively}*_", value=f"{{`{ctx.prefix}poll`}}", inline=True)
                    embed.add_field(name="_*quickpoll {Creates a Poll Quickly}*_", value=f"{{`{ctx.prefix}quickpoll <question> <answers>`}}", inline=True)
                    embed.add_field(name="_*restart(shutdown) {Restarts the Bot(Only Owner of the Bot can do this*_", value=f"{{`{ctx.prefix}restart/shutdown`}}", inline=True)

                    #embed.add_field(name="__**Commands:**__", value="_*invite(!invite #channelname)*_ - {Creates an invite for a specific channel}\n\n_*announce*_ - {Bot will say whatever the User says}\n\n_*dm*_ - {DM a User a custom message}\n\n_*poll*_ - {Creates a Poll}\n\n_*quickpoll*_ - {Creates a poll quickly}\n\n_*restart(shutdown)*_ - {Restart/Shutdown the Bot (Owner **Only**)}", inline=True)
                    
                    embed.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                    await m.edit(embed=embed)

                else:
                    if str(reaction.emoji) == '📖':
                        await m.remove_reaction('📖', member)
                        embed0 = discord.Embed(
                            title=f'All Commands (Default prefix is `{ctx.prefix}`)',
                            description="__**{{Command Index}}**__", 
                            color=discord.Color.darker_grey())

                        #embed0.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n♣️ __**General Commands**__ {Commands showing things such as serverinfo, userinfo, etc.}\n\n<:fun:734648757441921124> __**Fun Commands**__ {Variety of Different Fun Commands}\n\n<:grass:734647227523268668> __**Minecraft Commands**__ {Minecraft Related Fun Commands}\n\n🎉 __**Giveaway**__ {Commands for Giveaways}\n\n📑 __**Application Commands**__ {Commands to apply for something}\n\n📫 __**Suggestion Commands**__ {Commands to leave a Suggestion}\n\n🔐 __**Moderation Commands**__ {Commands to Moderate the server (Mods and Admins Only)}\n\n😱 __**Role Commands**__ {Commands for managing roles}\n\n🔗 __**Misc Commands**__ {Misc Commands Only Mods and Admins can Use}", inline=True)
                        embed0.set_footer(text="{{Please Remember This Bot is Not 100% Finished Yet}}")
                        embed0.add_field(name="📖 Main Menu", value="`Shows this Menu`", inline=True)
                        embed0.add_field(name="♠️ General Category", value="`List of General Commands`", inline=True)
                        embed0.add_field(name="<:fun:734648757441921124> Fun Category", value="`List of General Fun Commands`", inline=True)
                        embed0.add_field(name="<:grass:734647227523268668> Minecraft Category", value="`Fun Commands Related to Minecraft`", inline=True)
                        embed0.add_field(name="🎉 Giveaway Category", value="`List of Commands Related to Hosting Giveaways`", inline=True)
                        embed0.add_field(name="📚 Application/Suggestion Category", value="`List of Application/Suggestion Commands`", inline=True)
                        embed0.add_field(name="🔐 Moderation Category", value="`Commands Used to Moderate the Server`", inline=True)
                        embed0.add_field(name="😱 Roles Category", value="`Commands Used to Manage Roles in the Server`", inline=True)
                        embed0.add_field(name="🔗 Misc Category", value="`Miscallaneous Commands`", inline=True)
                        embed0.add_field(name="<:trash:734043301187158082> Cancellation", value="`Deletes this Embed/Help Message`", inline=True)
                        embed0.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                        await m.edit(embed=embed0)


def setup(bot):
    bot.add_cog(Help_Command(bot))
