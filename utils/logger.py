from utils.const import CONST

INFO = "INFO"
WARN = "WARNING"
ERR = "ERROR"
DEV = "DEV"
JSON = "JSON"


def log(log_type, msg):
    if isinstance(msg, list):
        for i in range(0, len(msg)):
            _print_log(msg[i], log_type)
    elif isinstance(msg, str):
        _print_log(msg, log_type)


def _print_log(msg: str, log_type):
    if log_type == DEV:
        if CONST.DEVMODE:
            print("[" + log_type + "]: " + msg)
    elif log_type == JSON:
        if not CONST.SUPPRESS_JSON_LOGGING:
            print("[" + log_type + "]: " + msg)
    else:
        print("[" + log_type + "]: " + msg)
