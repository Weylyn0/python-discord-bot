from time import time
from typing import Optional
from platform import python_version
from datetime import datetime, timedelta
from psutil import Process, virtual_memory

from discord import Embed, Member, __version__ as discord_version
from discord.ext.commands import Cog, command, guild_only

def utc_format(dt):
  return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

class Info(Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @command(name="userinfo", aliases=["ui"])
  async def cmd_userinfo(self, ctx, target:Optional[Member]):
    target = target or ctx.author
    embed = Embed(
      title="User Info",
      color=target.color,
      timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=target.avatar_url)
    embed.set_footer(text=ctx.message.guild.name)
    fields = [
      ("Username", str(target), False),
      ("ID", target.id, False),
      ("Bot", str(target.bot), True),
      ("Top Role", target.top_role.mention, True),
      ("Status", target.status.name, True),
      ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
      ("Created At", utc_format(target.created_at), False),
      ("Joined At", utc_format(target.joined_at), False)
    ]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)

  @command(name="serverinfo", aliases=["si"])
  @guild_only()
  async def cmd_serverinfo(self, ctx):
    embed = Embed(
      title=f"{ctx.guild.name} Server Info",
      color=ctx.guild.owner.color,
      timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=ctx.guild.icon_url)
    statuses = [
	    len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
	    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
	    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
      len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))
    ]
    fields = [
      ("ID", ctx.guild.id, True),
      ("Owner", ctx.guild.owner, True),
      ("Region", ctx.guild.region, True),
      ("Created At", utc_format(ctx.guild.created_at), True),
      ("Members", len(ctx.guild.members), True),
      ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
      ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
      ("Bans", len(await ctx.guild.bans()), True),
      ("Member Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
      ("Text Channels", len(ctx.guild.text_channels), True),
      ("Voice Channels", len(ctx.guild.voice_channels), True),
      ("Categories", len(ctx.guild.categories), True),
      ("Roles", len(ctx.guild.roles), True),
      ("Invites", len(await ctx.guild.invites()), True),
    ]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)

  @command(name="stats")
  async def cmd_stats(self, ctx):
    async with ctx.typing():
      start = time()
      msg = await ctx.send("-")
      end = time()
      dwsp_latency = round(self.bot.latency*1000)
      response_latency = round((end-start)*1000)
      proc = Process()
      with proc.oneshot():
        uptime = timedelta(seconds=time()-proc.create_time())
        cpu_time = timedelta(seconds=(cpu:=proc.cpu_times()).system + cpu.user)
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = round(mem_total * (mem_of_total / 100),2)
        mem_of_total = round(mem_of_total, 2)
        mem_total = round(mem_total/1024)
      embed=Embed(
        title=self.bot.user.name,
        color=ctx.guild.me.color if ctx.guild else ctx.author.color,
        timestamp=datetime.utcnow()
      )
      embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
      embed.set_thumbnail(url=self.bot.user.avatar_url)
      fields=[
	      ("Default Prefix", self.bot.prefix, True),
	      ("DWSP Latency", f"{dwsp_latency}ms", True), 
	      ("Response Latency", f"{response_latency}ms", True),
	      ("Bot Version", self.bot.VERSION, True),
	      ("Python Version", python_version(), True), 
	      ("Discord.py Version", discord_version, True),
	      ("Uptime", uptime, True),
	      ("CPU Time", cpu_time, True),
	      ("Loaded Cogs", len(self.bot.extensions), True),
	      ("Memory Usage", f"{mem_usage}MB/{mem_total}GB  {mem_of_total}%", False), 
	      ("Servers", len(self.bot.guilds), True),
        ("Users", len(self.bot.users), True),
        ("Banned Users", len(self.bot.banlist), True)]
      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
      await msg.delete()
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Info(bot))