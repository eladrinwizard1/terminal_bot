import json
import os
import subprocess
from typing import List

from discord import Message
from dotenv import load_dotenv

from lib import format_output
import json_tools as jtools

load_dotenv()
DATA = os.getenv("TERMINAL_BOT_DATA")


def change_directory(msg: Message) -> List[str]:
    message = msg.content.split(" ")
    if len(message) < 2:
        return ["Error: must pass path to `cd`"]
    try:
        os.chdir(
            os.path.expanduser(
                os.path.expandvars(
                    message[1]
                )
            )
        )
    except OSError:
        return [f"Error changing to path `{message[1]}`"]
    jtools.set_in_file(f"{DATA}/dirs.json",
                       f"{str(msg.guild)}/{str(msg.channel)}",
                       os.getcwd())
    process = subprocess.run("ls -p",
                             stdout=subprocess.PIPE,
                             universal_newlines=True,
                             shell=True)
    return format_output(f"cd {message[1]} && ls -p", process.stdout)


def print_file(msg: Message) -> List[str]:
    message = msg.content.split(" ")
    if len(message) < 2:
        return ["Error: must pass file name to `cat`"]
    extension = message[1].split(".")[-1]
    with open(f"{DATA}/extensions.json", "r") as f:
        extensions = json.load(f)
    language = extensions.get(extension, "Bash")
    process = subprocess.run(msg.content[1:],
                             stdout=subprocess.PIPE,
                             universal_newlines=True,
                             shell=True)
    return format_output(process.args, process.stdout,
                         process.stderr, language)


async def create_channel(msg: Message) -> List[str]:
    channels = [c.name for c in msg.guild.channels]
    try:
        category = next(c for c in msg.guild.categories
                        if c.name == "terminals")
    except StopIteration:
        category = await msg.guild.create_category("terminals")
    count = 1
    while f"terminal-{count}" in channels:
        count += 1
    channel = await category.create_text_channel(f"terminal-{count}")
    jtools.set_in_file(f"{DATA}/dirs.json",
                       f"{str(channel.guild)}/{str(channel)}",
                       os.getcwd())
    return [channel.mention]


async def delete_channel(msg: Message) -> List[str]:
    if "terminal-" in msg.channel.name:
        await msg.channel.delete()
    return []


# Dictionary of special functions to be called with !
FUNCTIONS = {
    "cd": change_directory,
    "cat": print_file
}


# Dictionary of async functions to be called with !
ASYNC_FUNCTIONS = {
    "start": create_channel,
    "end": delete_channel
}


# General parsing function
def parse_message(msg: Message) -> List[str]:
    """
    Parses a non-prefixed message from discord and returns result.
    :param msg: The message to parse.
    :return: The result to send as a Discord message.
    """
    process = subprocess.run(msg.content,
                             stdout=subprocess.PIPE,
                             universal_newlines=True,
                             shell=True)
    return format_output(process.args, process.stdout, process.stderr)
