from typing import Optional

from discord import Member
from discord.ext.commands import Cog, command, guild_only, has_permissions

class Mod(Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @command(name="kick")
  @guild_only() #This mean if a user try to invoke this command, bot will raise "NoPrivateChannel" error.
  @has_permissions(manage_guild=True)#And this is if user has not permissions(manage guild) in that server so bot will raise "CheckFailure" error.
  async def cmd_kick(self, ctx, member:Member, *, reason):
    """Kicks a user from server."""

    await ctx.guild.kick(member, reason=reason)
    await ctx.send(f"{member} has kicked from the server by {ctx.author.mention}")

  @command(name="ban")
  @guild_only()
  @has_permissions(manage_guild=True)
  async def cmd_ban(self, ctx, member:Member, *, reason):
    """Bans a member from your server."""
    
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"{member} has banned from the server by {ctx.author.mention}")

  @command(name="unban")
  @guild_only()
  @has_permissions(manage_guild=True)
  async def cmd_unban(self, ctx, *, user:str):
    """Removes a user's ban with his name and discriminator."""

    name = user.split("#")[0].strip()
    discriminator = user.split("#")[1]
    bans = await ctx.guild.bans()

    for entry in bans:
      banned_user = entry.user
      if banned_user.name == name and str(banned_user.discriminator) == discriminator:
        await ctx.guild.unban(banned_user)
        await ctx.send(f"{user}'s ban removed.")
    
    await ctx.send("This user already does not banned.")

  @command(name="clear")
  @guild_only()
  @has_permissions(manage_messages=True)
  async def cmd_clear(self, ctx, amount:Optional[int]=5):
    """Deletes message from a text channel in given amount."""

    await ctx.channel.purge(limit=amount+1)

def setup(bot):
  bot.add_cog(Mod(bot))