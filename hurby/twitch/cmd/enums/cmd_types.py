from enum import Enum


class CMDType(Enum):
    REPLY = "reply"
    ACTION = "action"
    MULTI_ACTION = "multi_action"
