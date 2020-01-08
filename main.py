import os
from typing import List

import discord

from parse import FUNCTIONS, ASYNC_FUNCTIONS, parse_message

# load environment variables
TOKEN = os.getenv('TERMINAL_BOT_TOKEN')
PREFIX = os.getenv("TERMINAL_BOT_PREFIX")

client = discord.Client()


@client.event
async def on_ready():
    """
    Runs when the bot finishes initialization.
    """
    os.chdir(os.path.expanduser("~"))
    print(f'{client.user} has connected to Discord!')
    channels = []
    for guild in client.guilds:
        channels += [channel for channel in guild.channels
                     if "terminal" in str(channel)]
    for channel in channels:
        await channel.send(
            f"terminal-bot is active on this channel with prefix {PREFIX}"
        )


# Parse messages

@client.event
async def on_message(message):
    """
    Runs each time a message is sent.
    """
    cmd = message.content.split(" ")[0][1:].lower()
    if message.author == client.user:
        return
    if type(message.channel) is discord.DMChannel or \
            "terminal" in str(message.channel):
        if message.content.startswith(PREFIX):
            fn = ASYNC_FUNCTIONS.get(cmd)
            if fn is None:
                fn = FUNCTIONS.get(cmd) or \
                     (lambda x: ["Error, command not found"])
                responses = fn(message)
            else:
                responses = await fn(message)
        else:
            fn = parse_message
            responses = fn(message)
        await message.delete()
        for response in responses:
            await message.channel.send(response)
    print(f"Message from {message.author}: {message.content}")

client.run(TOKEN)
