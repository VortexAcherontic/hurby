class IRCChatExtractor:

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
