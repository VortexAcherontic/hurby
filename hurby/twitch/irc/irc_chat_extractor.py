from hurby.twitch.irc.irc_cmd import IRCCommand


def extract_sender(line):
    result = ""
    for char in line:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def extract_message(line):
    result = ""
    i = 3
    length = len(line)
    while i < length:
        result += line[i] + " "
        i += 1
    result = result.lstrip(':')[0:-1]
    return result


def extract_command(msg):
    tmp = str.split(msg)
    cmd = IRCCommand(tmp[0], tmp[1:])
    return cmd
