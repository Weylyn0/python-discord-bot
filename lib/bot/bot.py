import os
from datetime import datetime

from discord import Intents #We are need to intents for getting members' and servers' detailed info. You can enable this on discord.com/developers/applications/<your_bot_id>/bot
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, BadArgument, Context

class Bot(BotBase):
  def __init__(self):
    self.prefix = "!" #Bot Prefix
    try:
      with open("./data/banlist.txt", "r") as f:
        self.banlist = [int(line) for line in f.readlines()]
    except FileNotFoundError:
      self.banlist = []
    super().__init__(command_prefix=self.prefix, intents=Intents.all())
  
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
  
  #Banlist save function
  def save_banlist(self):
    with open("./data/banlist.txt", "w") as f:
        f.writelines([str(user_id)+"\n" for user_id in self.banlist])
  
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
      raise error
  
  #Checking messsage author is bot or not
  async def on_message(self, message):
    if not message.author.bot:
      await self.process_commands(message)

  async def process_commands(self, message):
    ctx = await self.get_context(message, cls=Context)
    
    if ctx.command is not None and ctx.guild is not None: #Our commands is only for guilds.
      if message.author.id in self.banlist:
        await ctx.send("You are banned.")
        
      elif not self.is_ready():
        await ctx.send("I'm not ready to receive commands.")
      else:
        await self.invoke(ctx)

bot = Bot()