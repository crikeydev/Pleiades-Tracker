import logging
import discord
import os
from dotenv import load_dotenv
import a2s
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)

load_dotenv()

bot_token = str(os.getenv('TOKEN'))

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot()

def clean_string(input_str):      #the most scuffed implementation imaginable, but it works. Don't know why it refuses to clean \x01 so I had to physically split the string.
    chars_to_remove = '\x01⤳⬿'
    input_str = input_str.split("⤳")
    translation_table = str.maketrans('', '', chars_to_remove)
    cleaned_str = input_str[1].translate(translation_table)
    cleaned_str = cleaned_str.replace("server_name=", "").replace("'", "")
    cleaned_str = re.sub("\x01", "", cleaned_str)
    return cleaned_str
    
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[1068433342812389436])
async def hello(ctx):
    await ctx.respond("Gday mate, you suck!")

@bot.slash_command(guild_ids=[1068433342812389436])
async def retrieve(ctx, server):
    try:
        serverSplit = server.split(":")
        serverIP = str(serverSplit[0])
        serverPort = int(serverSplit[1])
    except: 
        await ctx.respond("An error occured, are you sure you put in a correct server address?")

    address = (serverIP, serverPort)

    try:
        serverInfo = a2s.info(address) # figure out how to properly implement the async version of this later
        serverInfoSplit = str(serverInfo).split(",")

        serverNameUnclean = serverInfoSplit[1]
        serverMapUnclean = serverInfoSplit[2]
        serverCurrentUnclean = serverInfoSplit[6]
        serverMaxUnclean = serverInfoSplit[7]

        serverNameClean = clean_string(str(serverNameUnclean))
        serverMapClean = str(serverMapUnclean).replace("map_name='", '').strip("'")
        serverCurrentClean = str(serverCurrentUnclean).replace("player_count=", '')
        serverMaxClean = str(serverMaxUnclean).replace("max_players=", '')
        serverPlayers = (serverCurrentClean + "/" + serverMaxClean).replace(" ", "")
        

        serverJoin = "[" + str(server) + "](https://connectsteam.me/?" + str(server) + ")" 

        embed = discord.Embed(
            title=serverNameClean,
            description="Now Playing: **" + serverMapClean + "**\nPlayers Online: **" + serverPlayers + "**\nQuick Join: **" + serverJoin + "**",
            timestamp=datetime.now()
        )

        await ctx.respond(embed=embed)
    except:
        await ctx.respond("An error occured when attempting to retrieve the server information. Please try again later! If the error persists, contact the bot creator!")


bot.run(bot_token)