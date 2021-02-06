from discord.ext.commands import Cog

class Example(Cog):
  def __init__(self, bot):
    self.bot = bot
    
  #This is a template for our cogs
  #We will be writing our commands in this cogs
  #The purpose of the cogs is to avoid confusion by categorizing commands
    
def setup(bot):
  bot.add_cog(Example(bot))