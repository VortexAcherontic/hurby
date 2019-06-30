from enum import Enum


class CMDResponseRealms(Enum):
    GLOBAL = "global"
    WHISPER = "whisper"


def get_realm(string: str):
    for s in CMDResponseRealms:
        if s == string:
            return s
