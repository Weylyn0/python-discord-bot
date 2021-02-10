from discord import Member
from discord.ext.commands import Cog, command, guild_only, has_permissions

class Mod(Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @command(name="kick")
  @guild_only() #This mean if a user try to invoke this command, bot will raise "NoPrivateChannel" error.
  @has_permissions(manage_guild=True)#And this is if user has not permissions(manage guild) in that server so bot will raise "CheckFailure" error.
  async def cmd_kick(self, ctx, member:Member, *, reason):
    await ctx.guild.kick(member, reason=reason)
    await ctx.send(f"{member} has kicked from the server by {ctx.author.mention}")

  @command(name="ban")
  @guild_only()
  @has_permissions(manage_guild=True)
  async def cmd_ban(self, ctx, member:Member, *, reason):
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"{member} has banned from the server by {ctx.author.mention}")

def setup(bot):
  bot.add_cog(Mod(bot))