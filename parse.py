from discord import Message
import subprocess
from lib import format_output

# Dictionary of special functions to be called with !
FUNCTIONS = {

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
