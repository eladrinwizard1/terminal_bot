import os

import discord

from parse import FUNCTIONS, ASYNC_FUNCTIONS, parse_message
import json_tools as jtools

# load environment variables
TOKEN = os.getenv('TERMINAL_BOT_TOKEN')
PREFIX = os.getenv("TERMINAL_BOT_PREFIX")
DATA = os.getenv('TERMINAL_BOT_DATA')

client = discord.Client()


@client.event
async def on_ready():
    """
    Runs when the bot finishes initialization.
    """
    print(f'{client.user} has connected to Discord!')
    channels = []
    for guild in client.guilds:
        channels += [channel for channel in guild.channels
                     if "terminal" in str(channel)]
        jtools.write_to_file(f"{DATA}/dirs.json",
                             {f"{str(guild)}/{str(channel)}":
                              os.path.expanduser("~") for channel in
                              guild.channels})
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
    if type(message.channel) is discord.DMChannel:
        return
    if "terminal" in str(message.channel):
        # Change to working directory of channel
        wd = jtools.read_file(f"{DATA}/dirs.json").get(
            f"{str(message.guild)}/{str(message.channel)}",
            os.path.expanduser("~"))
        os.chdir(wd)
        if message.content.startswith(PREFIX):
            fn = ASYNC_FUNCTIONS.get(cmd)
            if fn is None:
                fn = FUNCTIONS.get(cmd, lambda x: ["Error, command not found"])
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
