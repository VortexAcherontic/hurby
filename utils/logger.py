INFO = "INFO"
WARN = "WARNING"
ERR = "ERROR"


def log(type, msg):
    if isinstance(msg, list):
        for i in range(0, len(msg)):
            print("[" + type + "]: " + msg[i])
    elif isinstance(msg, str):
        print("[" + type + "]: " + msg)
