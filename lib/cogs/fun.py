from discord.ext.commands import Cog, command

import random

class Fun(Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @command(name="roll", aliases=["dice"])
  async def cmd_roll(self, ctx):
    """This command returns a random number between 1 and 6"""
    
    rolled=random.randint(1, 6) #We get a random number from 1 to 6
    await ctx.send(f"{ctx.author.name} rolled a dice and get {rolled}") #this is a f-string wich is allows to you use variables in a string
    
  @command(name="flip", aliases=["coin"])
  async def cmd_flip(self, ctx):
    """Flip a coin."""
    
    #The ctx parameter is a Context object wich we can get message's server, content, author, channel and also send message to this channel
    
    sides=["heads", "tails"]
    await ctx.send(f"{ctx.author.name} flipped a coin and get {random.choice(sides)}")
    
def setup(bot):
  bot.add_cog(Fun(bot))