import os
import discord
from dotenv import load_dotenv
from parser import FUNCTIONS, DMFUNCTIONS, parse_message

# load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv("PREFIX")

client = discord.Client()

CHANNELS = []  # the channels on which to operate


@client.event
async def on_ready():
    """
    Runs when the bot finishes initialization.
    """
    print(f'{client.user} has connected to Discord!')
    global CHANNELS
    for guild in client.guilds:
        CHANNELS += [channel for channel in guild.channels
                     if "terminal" in str(channel)]
    for channel in CHANNELS:
        await channel.send(
            f"terminal-bot is active on this channel with prefix {PREFIX}"
        )


# parse Discord messages


@client.event
async def on_message(message):
    """
    Runs each time a message is sent.
    """
    if message.author == client.user:
        return
    elif type(message.channel) is discord.DMChannel:
        fn = DMFUNCTIONS.get(message.content.split(" ")[0][1:].lower(),
                             lambda x: "Error: no such command found")
    elif message.channel not in CHANNELS:
        return
    elif not message.content.startswith(PREFIX):
        fn = parse_message
    else:
        fn = DMFUNCTIONS.get(message.content.split(" ")[0][1:].lower(),
                             lambda x: "Error: no such command found")
    if fn is not None:
        response = fn(message)
        await message.channel.send(response)
    print(f"Message from {message.author}: {message.content}")

client.run(TOKEN)
