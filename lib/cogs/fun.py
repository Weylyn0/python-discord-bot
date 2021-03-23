import random
import aiohttp

from discord import Embed
from discord.ext.commands import Cog, command

class Fun(Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @command(name="flip", aliases=["coin"])
  async def cmd_flip(self, ctx):
    """Flip a coin."""
    
    #The ctx parameter is a Context object wich we can get message's server, content, author, channel and also send message to this channel
    
    sides=["heads", "tails"]
    await ctx.send(f"{ctx.author.name} flipped a coin and get {random.choice(sides)}") #this is a f-string wich is allows to you use variables in a string
  
  @command(name="roll", aliases=["dice"])
  async def cmd_roll(self, ctx, dice_string:str):
    """Dice in given max value and amount."""
    
    try:
      dice, value = (int(num) for num in dice_string.split("d"))
    except:
      return await ctx.send("You did not enter any value for roll.")
    if dice <= 25:
      rolls = [random.randint(1, value) for i in range(dice)]
      await ctx.send(" + ".join([str(r) for r in rolls]) + " = " + str(sum(rolls)))
    else:
      await ctx.send("I can't roll that many dice. Please try a lower number.")
  
  @command(name="echo", aliases=["say"])
  async def cmd_echo(self, ctx, *, message):
    """Repeats a message."""
  
    await ctx.message.delete()
    await ctx.send(message)
  
  @command(name="fact")
  async def cmd_fact(self, ctx):
    """Returns a random animal fact."""

    animals = ("cat", "dog", "panda", "fox", "bird", "coala")
    animal = random.choice(animals)
    url = "https://some-random-api.ml/facts/" + animal
    img_url = "https://some-random-api.ml/img/" + animal if animal!="bird" else "birb"
    async with aiohttp.ClientSession() as ses:
      async with ses.get(url) as r:
        fact_message = await r.json()
        fact_message = fact_message.get("fact")
      async with ses.get(img_url) as r:
        img = await r.json()
        img = img.get("link")
    emb = Embed(
      description=fact_message,
      color=ctx.author.color
    )
    emb.set_image(url=img)
    await ctx.send(embed=emb)

def setup(bot):
  bot.add_cog(Fun(bot))