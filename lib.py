from typing import List

MESSAGE_LIMIT = 1900


def _wrap(content: str, language: str = "Bash") -> str:
    """
    Wraps a Discord message in a codeblock with appropriate syntax highlighting.
    :param content: The message content.
    :param language: The language to highlight syntax for. Default `Bash`.
    :return: A Discord codeblock.
    """
    return f"```{language}\n{content}\n```"


def _split(content: str) -> List[str]:
    """
    Splits longer messages into valid-length messages for Discord.
    :param content: The message to split.
    :return: A list of messages short enough for Discord.
    """
    lines = content.split("\n")
    lines.reverse()
    output = []
    current = ""
    while len(lines) > 0:
        line = lines.pop()
        if len(line) > MESSAGE_LIMIT:
            lines.append(line[:MESSAGE_LIMIT])
            lines.append(line[MESSAGE_LIMIT:])
        elif len(current) + len(line) < MESSAGE_LIMIT:
            current += f"\n{line}"
        else:
            output.append(f"{current}\n")
            current = line
    output.append(current)
    return output


def format_output(content: str, stdout: str = None, stderr: str = None,
                  language: str = "Bash") -> List[str]:
    """
    Formats the input and response from a command for display in Discord.
    :param content: The input message from the user.
    :param stdout: The stdout response to running the input.
    :param stderr: The stderr response to running the input.
    :param language: The language to highlight syntax for.
    :return: The formatted Discord block message.
    """
    output = f"$ {content}\n"
    output += f"{stdout}\n"
    # TODO: fix this formatting
    if stderr is not None:
        output += f"stderr:\n {stderr}\n"
    return [_wrap(msg, language) for msg in _split(output)]
