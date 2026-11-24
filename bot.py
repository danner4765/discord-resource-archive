import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="$",
    intents=intents
)


async def load_extensions():
    await bot.load_extension("cogs.resources")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Resource Archive is online!")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


import asyncio
asyncio.run(main())
