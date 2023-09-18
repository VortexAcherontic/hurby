from datetime import datetime

from utils.const import CONST

INFO = "INFO"
WARN = "WARNING"
ERR = "ERROR"
DEV = "DEV"
JSON = "JSON"
FATAL = "FATAL"
__hurby = None


def init_logger(hurby):
    __hurby = hurby


def log(log_type, msg):
    if isinstance(msg, list):
        for i in range(0, len(msg)):
            _print_log(msg[i], log_type)
    elif isinstance(msg, str):
        _print_log(msg, log_type)


def _print_log(msg: str, log_type):
    time = datetime.now()
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    d1 = datetime.strptime(str(time), fmt)
    text = str(d1) + ": [" + log_type + "]: " + msg
    if log_type == DEV:
        if CONST.DEVMODE:
            print(text)
    elif log_type == JSON:
        if not CONST.SUPPRESS_JSON_LOGGING or CONST.DEVMODE:
            print(text)
    elif log_type == ERR or log_type == FATAL or log_type == WARN:
        print(text)
        _append_to_log_file(text)
    else:
        print(text)


def _append_to_log_file(msg: str):
    log_file_path = CONST.DIR_APP_DATA_ABSOLUTE + "/" + CONST.FILE_LOG
    if CONST.DEVMODE:
        log_file = open(log_file_path, "a", encoding="utf-8")
        log_file.write(msg + "\n")
        log_file.close()
