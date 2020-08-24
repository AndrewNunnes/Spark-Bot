import discord
from discord.ext import commands
import aiosqlite 
from aiosqlite import connect

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        #self.bot.db refers to
        #bot.db under connect_db
        #In Maine File
        self.db = self.bot.db
        
#•--------------------------------•
        
#STATEMENTS
#fetchone() : Only used when fetching one row
#fetchmany() : Used when fetching multiple rows
#executescript(): 
#commit() : Save data to database
#close : Close database connection 
  #-{To make sure we don't have a bunch of them open}

#QUERIES
#INTEGER : Digit
#FLOAT : Numbers as floats
#PRIMARY KEY : 
#FOREIGN KEY : 
#NULL : something that is not set
#TEXT : Used for text

#TABLES STATEMENTS
#SELECT : Selecting a column from a table
#SELECT * : Select all columns
#INSERT INTO : Inserting new data into a column
#DELETE FROM : Deleting data from a column
#DISTINCT :

#•----------Functions----------•#
    
    #Used to close the database connection
    async def close(self):
      
        return await self.db.close()
        
    #Used to commit (save) changes to database
    async def commit(self):
      
        return await self.db.commit()
    
    #Used to get database cursor
    #execute returns a cursor
    async def execute(self, sql, *param):
      
        return await self.db.execute(sql, param)
        
#•----------Welcome/Goodbye System----------•%
        
    #Function to set welcome channel
    async def welcome_channel(self, gid, cid):
      
        result = await (await self.execute("SELECT channel_id FROM welcome WHERE guild_id = ?", gid)).fetchone()
        
        if result is None:
            await self.execute("INSERT INTO welcome(guild_id, channel_id) VALUES(?, ?)", gid, cid)
            
        elif result is not None:
            await self.execute("UPDATE welcome SET channel_id = ? WHERE guild_id = ?", cid, gid)
            
        await self.commit()
        
        return result
        #await self.close()
        
    #Function to set goodbye channel
    async def goodbye_channel(self, gid, cid):
        
        result = await (await self.execute("SELECT channel_id FROM goodbye WHERE guild_id = ?", gid)).fetchone()
        
        if result is None:
            await self.execute("INSERT INTO welcome(guild_id, channel_id) VALUES(?, ?)", gid, cid)
        elif result is not None:
            await self.execute("UPDATE goodbye SET channel_id = ? WHERE guild_id = ?", cid, gid)
            
        await self.commit()
        
        return result
        
    #Function to set welcome text
    async def welcome_text(self, gid, w_text):
        
        result = await (await self.execute("SELECT msg FROM welcome WHERE guild_id = ?", gid)).fetchone()
        
        if result is None:
            await self.execute("INSERT INTO welcome(guild_id, msg) VALUES(?, ?)", gid, w_text)
            
        elif result is not None:
            await self.execute("UPDATE welcome SET msg = ? WHERE guild_id = ?", w_text, gid)
            
        await self.commit()
        
        return result
        #await self.close()
    
    #Function to set goodbye text
    async def goodbye_text(self, gid, g_text):
        
        result = await (await self.execute("SELECT msg FROM goodbye WHERE guild_id = ?", gid)).fetchone()
        
        if result is None:
            await self.execute("INSERT INTO goodbye(guild_id, msg) VALUES(?, ?)", gid, g_text)
        
        elif result is not None:
            await self.execute("UPDATE goodbye SET msg = ? WHERE guild_id = ?", g_text, gid)
            
        await self.commit()
        
        return result
        
    #Function to get the set welcome message
    async def get_w_text(self, gid):
        
        result = await (await self.execute("SELECT msg FROM welcome WHERE guild_id = ?", gid)).fetchone()
        print(result)
        
        await self.commit()
       # await self.close()
        
        return result[0]
        
    #Function to get the set goodbye message
    async def get_g_text(self, gid):
        
        result = await (await self.execute("SELECT msg FROM goodbye WHERE guild_id = ?", gid)).fetchone()
        print(result)
        
        await self.commit()
       # await self.close()
        
        return result[0]
        
    #Function to delete set welcome message
    async def remove_w_text(self, gid):
        
        #Delete the custom message
        #From the database
        result = await self.execute("UPDATE welcome SET msg = NULL WHERE guild_id = ?", gid)
        print(result)

        await self.commit()
        
        return result
        
    #Function to delete set goodbye message
    async def remove_g_text(self, gid):
        
        #Delete the set message from database
        #From the database
        result = await self.execute("UPDATE goodbye SET msg = NULL WHERE guild_id = ?", gid)
        print(result)
        
        await self.commit()
        
        return result
        
#•----------Mute/Unmute System----------•#
    
    #Function to insert the 
    #Targets id, role id, and end time
    async def mute_members(self, trgt, rid, endtm):
        
        result = await self.execute("INSERT OR IGNORE INTO mutes(user_id, role_id, end_time) VALUES(?, ?, ?)", trgt, rid, endtm)
        #print(result)
        
        await self.commit()
        
        return result
    
    #Function to get the target's role ids
    async def get_roles(self, uid):
        
        result = await (await self.execute("SELECT role_id FROM mutes WHERE user_id = ?", uid)).fetchone()
        #print(result)
        
        await self.commit()
        
        return result
        
    #Function to unmute the member
    async def unmute_member(self, uid):
        
        result = await self.execute("DELETE FROM mutes WHERE user_id = ?", uid)

        await self.commit()
        
        return result

#•----------Prefix System----------•#
  
    #Function to get prefix
    async def get_prefix(self, gid):
        
        result = await (await self.execute("SELECT prefix FROM prefix_list WHERE guild_id = ?", gid)).fetchone()
        
        #If there is no prefix set
        #Return default
        if result is None:
            return "!"
        #Else if there is a set prefix
        #Return that
        else:
            return result[0]
        
        await self.commit()
        await self.close()
        
        return result

    #Function to set the prefix   
    async def set_prefix(self, gid, prefix):
  
        result = await (await self.execute("SELECT prefix FROM prefix_list WHERE guild_id = ?", gid)).fetchone()
        
        if result is None:
            await self.execute("INSERT INTO prefix_list(guild_id, prefix) VALUES(?, ?)", gid, prefix)
        elif result is not None:
            await self.execute("UPDATE prefix_list SET prefix = ? WHERE guild_id = ?", prefix, gid)
        
        await self.commit()
        await self.close()
        
        return result
    
    #Function to set the prefix
    async def delete_prefix(self, gid):

        #Set the prefix column to Null
        c = await self.execute("UPDATE prefix_list SET prefix = NULL WHERE guild_id = ?", gid)

        await self.commit()
        await self.close()
        
        return c
        
#•----------Warn System----------•#
  
    #Function to add warns
    #And save to database
    async def add_warns(self, uid, modid, reason, gid):
    
        #Add warns to users
        c = await self.execute("INSERT OR IGNORE INTO warns (user_id, mod_id, reason, guild_id) VALUES (?, ?, ?, ?)", uid, modid, reason, gid)
    
        await self.commit()
        await self.close()
        
        return c
    
    #Function to get all user warns
    #For specific guild and user ids
    async def get_warns(self, uid, gid):
      
        c = await (await self.execute("SELECT * FROM warns WHERE user_id = ? AND guild_id = ?", uid, gid)).fetchone()
    
        await self.commit()
        await self.close()
        
        return c

    #Function to clear all user warns
    async def clear_warns(self, uid, gid):

        c = await self.execute("DELETE FROM warns WHERE user_id = ? AND guild_id = ?", uid, gid)
    
        await self.commit()
        await self.close()
        
        return c

def setup(bot):
    bot.add_cog(Database(bot))
