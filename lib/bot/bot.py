from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, BadArgument

from datetime import datetime
import os

class Bot(BotBase):
  def __init__(self):
    self.prefix = "!" #Bot Prefix
    super().__init__(command_prefix=self.prefix)
  
  #Loading our cogs
  def setup(self):
    for filename in os.listdir("./lib/cogs"):
      if filename.endswith(".py"):
        self.load_extension(f"lib.cogs.{filename[:-3]}")
  
  #Run bot
  def run(self, VERSION):
    self.VERSION = VERSION
    self.setup()
    TOKEN = os.getenv('TOKEN') #token on the .env file
    super().run(TOKEN)
  
  #on connect event
  async def on_connect(self):
    print("---Starting Bot---")
    print(f"Time: {datetime.utcnow()}")
    print(f"Servers: {len(self.guilds)}")
    print(f"Users: {len(self.users)}")
  
  #on ready event
  async def on_ready(self):
    print(f"We are logged in as {self.user}")
  
  #Error handling
  async def on_command_error(self, ctx, error):
    if isinstance(error, CommandNotFound):
      return
    elif isinstance(error, MissingRequiredArgument):
      await ctx.send("Some required arguments are missing.")
    elif isinstance(error, BadArgument):
      await ctx.send("Malformed Argument")
    else:
      await ctx.send("An error occured.")
    
bot = Bot()