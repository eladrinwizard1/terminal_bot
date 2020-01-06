from discord import Message
import subprocess
from lib import format_output
import os


def change_directory(msg: Message) -> str:
    message = msg.content.split(" ")
    if len(message) < 2:
        return "Error: must pass path to `cd`"
    try:
        os.chdir(message[1])
    except OSError:
        return f"Error changing to path `{message[1]}`"
    process = subprocess.run("ls",
                             stdout=subprocess.PIPE,
                             universal_newlines=True,
                             shell=True)
    return format_output(f"cd {message[1]} && ls", process.stdout)


def print_file(msg: Message) -> str:
    message = msg.content.split(" ")
    if len(message) < 2:
        return "Error: must pass file name to `cat`"
    extension = message[1].split(".")[-1]
    # TODO: add more extensions and store this data elsewhere
    extensions = {
        "py": "Python",
        "c": "C",
        "c0": "C",
        "c++": "C++",
        "js": "JavaScript",
        "json": "JavaScript",
        "html": "HTML",
        "md": "Markdown"
    }
    language = extensions.get(extension, "Bash")
    process = subprocess.run(msg.content[1:],
                             stdout=subprocess.PIPE,
                             universal_newlines=True,
                             shell=True)
    return format_output(f"cd {message[1]} && ls", process.stdout)

# Dictionary of special functions to be called with !
FUNCTIONS = {
    "cd": change_directory,
    "cat": print_file
}

# Dictionary of special (direct message) functions to be called with !
DMFUNCTIONS = {

}


# General parsing function
def parse_message(msg: Message) -> str:
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
