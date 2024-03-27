import os
import discord
from discord import option
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)

load_dotenv()

@bot.event
async def on_ready():
    print(f"[slashcommands] => Registered {len(bot.commands)} slashcommands : {[command.name for command in bot.commands]}")
    print(f"Logged in as {bot.user}")

@bot.slash_command(name = "ping", description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {round(bot.latency * 1000)}ms")

@bot.slash_command(name = "scan", description="Scan all the ports of a server to find open ports.")
@option("server", description="Server name", type=str)
@option("start_port", description="Start port", type=int, required=False, default=1)
@option("end_port", description="End port", type=int, required=False, default=65535)
async def scan(ctx, server, start_port, end_port):
    msg = await ctx.respond("Scanning...")


bot.run(os.getenv('TOKEN'))