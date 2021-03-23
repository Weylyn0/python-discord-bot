from discord import User
from discord.utils import get
from discord.ext.commands import Cog, command, is_owner, Greedy

class Owner(Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @command(name="!ban") #I want to distinguish this commands from others so we will use another exclamation mark for this. We will type this like "!!ban"
  @is_owner() #This is check for user is bot's owner
  async def cmd_owner_ban(self, ctx, targets:Greedy[User]=None): #We are using Greedy for banning or unbanning multiple users
    banned_users = []
    for target in targets:
      if target.id not in self.bot.banlist:
        self.bot.banlist.append(target.id)
        banned_users.append(target)
    self.bot.save_banlist()
    await ctx.send(", ".join(str(user) for user in banned_users) + " are banned.")
  
  @command(name="!unban")
  @is_owner()
  async def cmd_owner_unban(self, ctx, targets:Greedy[User]=None):
    unbanned_users = []
    for target in targets:
      if target.id in self.bot.banlist:
        self.bot.banlist.remove(target.id)
        unbanned_users.append(target)
    self.bot.save_banlist()
    await ctx.send(", ".join(str(user) for user in unbanned_users) + " are unbanned.")
  
  @command(name="!toggle")
  @is_owner()
  async def cmd_owner_toggle(self, ctx, *, cmd:str):
    if cmd:=get(self.bot.commands, name=cmd):
      cmd.enabled = not cmd.enabled
      state = " enabled." if cmd.enabled else " disabled."
      await ctx.send(str(cmd) + state)
    else:
      await ctx.send("I did not find that command.")

def setup(bot):
  bot.add_cog(Owner(bot))