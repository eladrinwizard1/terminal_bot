def format_output(content: str, stdout: str = None, stderr: str = None,
                  language: str = "Bash") -> str:
    """
    Formats the input and response from a command for display in Discord.
    :param content: The input message from the user.
    :param stdout: The stdout response to running the input.
    :param stderr: The stderr response to running the input.
    :param language: The language to highlight syntax for.
    :return: The formatted Discord block message.
    """
    output = f"```{language}\n"
    output += f"$ {content}\n"
    output += f"{stdout}\n"
    # TODO: fix this formatting
    if stderr is not None:
        output += f"stderr:\n {stderr}\n"
    output += "```"
    return output
