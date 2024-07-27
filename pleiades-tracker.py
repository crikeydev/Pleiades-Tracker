import logging
import discord
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

bot_token = str(os.getenv('TOKEN'))

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[1068433342812389436])
async def hello(ctx):
    await ctx.respond("Gday mate, you suck!")

bot.run(bot_token)